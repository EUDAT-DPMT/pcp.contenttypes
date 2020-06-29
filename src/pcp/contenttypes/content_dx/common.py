"""Common components shared by content types
"""
from incf.countryutils.datatypes import Country
from plone.app.textfield.interfaces import ITransformer
from plone.app.uuid.utils import uuidToObject
from zope.component.hooks import getSite
from zope.globalrequest import getRequest

import math

END_OF_EUDAT2020 = "2018-02-28"


class OfferUtilities(object):
    """
    Mixin class to provide shared functionality across offer types
    such as aggregated constraints
    """

    def aggregated_constraints(self):
        """Formated string summarizing all constraints"""

        transformer = ITransformer(self)

        regional = self.regional_constraints
        thematic = self.thematic_constraints
        organizational = self.organizational_constraints
        general_constraints = self.constraints
        if general_constraints is not None:
            general = transformer(self.constraints, 'text/plain')
        else:
            general = ''

        result = ''

        if regional:
            result += "<em>Regional:</em> %s <br />" % regional
        if thematic:
            result += "<em>Thematic:</em> %s <br />" % thematic
        if organizational:
            result += "<em>Organizational:</em> %s <br />" % organizational
        if general:
            result += general[:60]

        return result


class RequestUtilities(object):
    """Mixin class to provide shared functionality across request types"""

    def request_details(self):
        """Helper method used for string interpolation"""
        values = []
        compute = self.getCompute_resources()
        storage = self.getStorage_resources()
        if compute:
            for c in compute:
                formatted = self.comp2string(c)
                values.append("Compute: " + formatted)
        if storage:
            for s in storage:
                formatted = self.storage2string(s)
                values.append("Storage: " + formatted)
        return "\n".join(values)

    def comp2string(self, comp):
        template = "{nCores} Cores, {ram} RAM, {diskspace} disk, {system}"
        return template.format(**comp)

    def storage2string(self, storage):
        storage['class'] = storage.get('storage class','(not specified)')
        template = "{value} {unit} {class}"
        return template.format(**storage)

    def providers2string(self):
        """Helper method used for string interpolation"""
        providers = self.getPreferred_providers()
        if not providers:
            return "not specified"
        return ", ".join([p.Title() for p in providers])

    def users_to_notify(self):
        """Email addresses to be notified infered from the preferred providers"""
        try:
            providers = self.getPreferred_providers()
        except AttributeError:
            portal = getSite()
            providers = self.__of__(portal).getPreferred_providers()
        if not providers:
            return ''
        contacts = []
        for provider in providers:
            operations_contact = provider.getContact()
            business_contact = provider.getBusiness_contact()
            if operations_contact:
                contacts.append(operations_contact.getEmail())
            if business_contact:
                contacts.append(business_contact.getEmail())
        return contacts


class CommonUtilities(object):
    """Mixin class to provide shared functionality across content types"""

    def identifierTypes(self, instance):
        """Controlled vocabulary for the supported PID systems"""

        return ateapi.getDisplayList(instance, 'identifier_types', add_select=True)

    def ids(self):
        """Tuple of all identifiers - from the field plus uid and pid"""
        ids = [entry.get('value', '') for entry in self.identifiers]
        ids.append(self.UID())
        handle = None  # self.handle_client._getHandle(self)
        if handle is not None:
            ids.append(handle)
        return tuple(ids)

    # replace with a default schema field...
    # def country(self):
    #     """
    #     Look for the country in the address field including the aq_parent
    #     for indexing. Returns 'not set' if nothing found. Should not fail.
    #     """
    #     try:
    #         address = self.address
    #     except AttributeError:
    #         try:
    #             address = self.aq_parent.address
    #         except AttributeError:
    #             return "not set"
    #     return address.get('country', 'not set')

    def country_code(self):
        """Two letter country code infered from the address - if found"""
        country = self.country
        if not country:
            return
        # a hard-coded exception
        if country == "United Kingdom":
            return "UK"
        return Country(country).alpha2

    def additional_content(self):
        """Values of the additional key/value pairs for indexing"""
        content = []
        for entry in self.additional:
            content.append(entry.get('key', ''))
            content.append(entry.get('value', ''))
        return ' '.join(content)

    def stateIn(self, states):
        """Helper method to control visibility of fields"""
        review_state = self.portal_workflow.getInfoFor(self, 'review_state')
        return review_state in states

    def stateNotIn(self, states):
        """Helper method to control visibility of fields"""
        review_state = self.portal_workflow.getInfoFor(self, 'review_state')
        return review_state not in states

    def PID(self):
        """Return the handle PID if existing; None otherwise"""
        return None
        return self.handle_client._getHandle(self)

    def getStorage_resources(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['storage_resources'].get(self)
        converted = []
        for item in raw:
            if not item.get('value', None):
                continue
            converted.append(self.convert(item))
        return converted

    # Service offer and request types need this enhanced mutator

    def setService_option(self, value):
        """
        Custom mutator to set the linked service in addition
        """
        self.schema['service_option'].set(self, value)
        # now infer the service from the service option
        # this assumes that the service is the "grandparent"
        # of the selected service option
        option = uuidToObject(value)
        if option is None:
            self.schema['service'].set(self, [])
        else:
            service = option.unrestrictedTraverse("../..")
            try:
                self.schema['service'].set(self, service.UID())
            except KeyError:
                pass


    # Enable backlinks to the central registry

    url_pattern = 'https://creg.eudat.eu/view_portal/index.php?Page_Type=%s&id=%s'

    # Type mapping (DP -> CREG)
    dptype2cregtype = {
        "provider_dx": "Site",
        "registeredservice_dx": "Service_Group",
        "registeredservicecomponent_dx": "Service",
    }

    def getCregId(self, id_key='creg_id'):
        """
        Looks up the 'id_key' in the list of 'additional' KV pairs
        and returns its value if found. Otherwise returns None.
        """
        for entry in self.additional:
            if not entry.has_key('key'):
                return None
            if entry['key'] == id_key:
                return entry['value']
        return None

    def getCregURL(self, url_only=False):
        """
        Returns an anchor tag with the annotated URL to the
        corresponding entry in EUDAT's central registry if
        it can be constructed.
        Returns an explanatory message otherwise.
        If 'url_only' is True it just returns the URL.
        """
        creg_id = self.getCregId()
        if creg_id in [None, '']:
            return "No 'creg_id' found"
        try:
            ctype = self.dptype2cregtype[self.portal_type]
        except KeyError:
            return "No corresponding type known"
        url = self.url_pattern % (ctype, creg_id)
        if url_only:
            return url
        title = 'Link to the corresponding entry in the central registry'
        anchor = "<a href='%s' title='%s' target='_blank'>%s</a>" % (
            url, title, url)
        return anchor

    def convert(self, raw, target_unit='auto'):
        """Checking REQUEST for a target unit and converting
        if necessary
        """
        request = getRequest()
        target_unit = request.get('unit', target_unit)
        return self.convert_pure(raw, target_unit)

    def convert_pure(self, raw, target_unit='auto'):
        """Convert value to target_unit.
           If a particular target_unit (i.e. in unit_map) is stated then convert to that.
           If target_unit == 'auto' then determine a unit that is 'human readable'.
           If target_unit is None then keep current unit.
        """
        if raw is None:
            return raw

        raw = raw.copy()

        v = raw.get('value', '')
        u = raw.get('unit', '')
        result = {'value': v,
                  'unit': u,
                  }

        try:
            # ensure valid target unit
            if target_unit in unit_map:
                pass
            elif target_unit in (None, 'auto'):
                pass
            else:
                # invalid value: fall back to human readable
                target_unit = 'auto'

            # determine target unit if necessary
            if target_unit == 'auto':
                value = self.pint_convert(float(v or '1') or 1.0, u, 'B')['value']

                units_2 = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB',)
                units_10 = ('B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB',)

                if u in units_2 or u in ('byte', 'bit'):
                    unit_magnitude = int(math.log(value, 1024))
                    units = units_2
                else:
                    unit_magnitude = int(math.log(value, 1000))
                    units = units_10

                unit_index = max(0, min(len(units) - 1, unit_magnitude))
                target_unit = units[unit_index]
            elif target_unit is None:
                target_unit = u
            else:  # in unit_map
                pass

            # convert value to target unit
            if target_unit != u:
                result = self.pint_convert(v, u, target_unit)
        except KeyError:
            pass  # no target unit specified

        raw.update(result)
        return raw

    def pint_from_dict(self, d):
        """ Convert one of our memory quantity dicts to pint. """
        try:
            return float(d['value']) * unit_map[d['unit']]
        except ValueError:
            # Can happen if 'value' is a non-castable string
            return 0.0 * unit_map[d['unit']]

    def pint_to_dict(self, p):
        """ Convert a pint memory quantity to one of our dicts. """
        return dict(value=str(p.magnitude), unit=unit_map_inverse[p.units])

    def pint_add_dicts(self, values):
        """ Sum all values in our memory quantity dict format using pint. """
        return self.pint_to_dict(
            sum(
                map(lambda d: self.pint_from_dict(d), values),
                0 * ur.byte))

    def getStorageResourcesUsedSummary(self, resources):
        """ Get sum of all resources' usage. If this value can not be determined
            (i.e. some resource's values are not available) then None is returned.
        """
        from pcp.contenttypes.content_dx.registeredstorageresource import IRegisteredStorageResource
        usages = []

        for resource in resources:
            if IRegisteredStorageResource.providedBy(resource):
                used = resource.getUsedMemory()
                if used:
                    usages.append(used['core'])
                else:
                    return None

        return self.pint_add_dicts(usages)

    def getStorageResourcesSizeSummary(self, resources):
        """ Get sum of all resources' size. If this value can not be determined
            (i.e. size of a resource is not available) then None is returned.
        """
        from pcp.contenttypes.content_dx.registeredstorageresource import IRegisteredStorageResource
        sizes = []

        for resource in resources:
            if IRegisteredStorageResource.providedBy(resource):
                size = resource.getAllocatedMemory()
                if size:
                    sizes.append(size)
                else:
                    return None

        return self.pint_add_dicts(sizes)

    def renderMemoryValue(self, d):
        if not d:
            return ""
        try:
            d = self.convert(d)
        except ValueError:
            return ""
        request = getRequest()
        value = float(d['value'])
        unit = d['unit'] if request.get('unit') not in unit_map else ''
        return '%0.2f %s' % (value, unit)

    def renderResourceUsage(self, used, size):
        """ Render resource usage string.
        """
        if size:
            size = self.convert(size)
            size_value = float(size['value'])
            size_unit = size['unit']
            size_str = '%0.2f %s' % (size_value, size_unit)
        else:
            size_str = '??'
            size_value = None
            size_unit = None

        if used:
            core_in_size_unit = self.convert(used, size_unit)
            core_value_in_size_unit = float(core_in_size_unit['value'])
            used = self.convert(used)
            core_value = float(used['value'])
            used_str = '%0.2f %s' % (core_value, used['unit'])
        else:
            core_value = None
            used_str = '??'

        if core_value and size_value:
            rel_usage_str = '%0.2f' % (core_value_in_size_unit / size_value * 100.0)
        else:
            rel_usage_str = '??'

        return '%s / %s (%s%%)' % (used_str, size_str, rel_usage_str)

    def getResourceUsageSummary(self, resources):
        """ Create usage summary for resources. """
        used = self.getStorageResourcesUsedSummary(resources)
        size = self.getStorageResourcesSizeSummary(resources)

        return self.renderResourceUsage(used, size)

    def listResourceUsage(self, resources):
        """ List usage of resources, i.e. all resource's usage. """
        from pcp.contenttypes.content_dx.registeredstorageresource import IRegisteredStorageResource
        usages = []
        for resource in self.getResources():
            if IRegisteredStorageResource.providedBy(resource):
                usages.append('%s: %s' % (resource.title, resource.getResourceUsage()))

        return '<br>'.join(usages)

    def registeredObjectsTotal(self):
        """ Sum of all registered objects across related registered storage resources """
        from pcp.contenttypes.content_dx.registeredstorageresource import IRegisteredStorageResource
        total = 0
        for resource in self.getResources():
            if IRegisteredStorageResource.providedBy(resource):
                total += resource.getNumberOfRegisteredObjects(as_int=True)

        return total

    def pint_convert(self, value, from_unit, to_unit):
        """Helper function doing unit conversions using Pint"""

        source_unit = unit_map[from_unit]
        target_unit = unit_map[to_unit]

        source = float(value) * source_unit
        target = source.to(target_unit)

        result = {'value': target.magnitude,
                  'unit': to_unit,
                  }

        return result

    def yesno(self, instance):
        """Seems like RecordsFields do not support checkboxes"""
        return atapi.DisplayList([['', 'Select'], ['yes', 'yes'], ['no', 'no']])

    def sizeToString(self, size):
        if size:
            try:
                return '%0.2f %s' % (float(size['value']), size['unit'])
            except (ValueError, KeyError):
                return 'invalid size'
        else:
            return 'unknown size'

# we don't want to use eval so we define an explicit mapping of supported units

from pint import UnitRegistry
ur = UnitRegistry()

unit_map = {'bit': ur.bit,
            'kb':  ur.kilobit,
            'byte': ur.byte,
            'B':   ur.byte,
            'kB':  ur.kilobyte,
            'Kb':  ur.kilobyte,  # handle a nasty typo in an accounting record
            'MB':  ur.megabyte,
            'GB':  ur.gigabyte,
            'TB':  ur.terabyte,
            'PB':  ur.petabyte,
            'EB':  ur.exabyte,
            'KiB': ur.kibibyte,
            'MiB': ur.mebibyte,
            'GiB': ur.gibibyte,
            'TiB': ur.tebibyte,
            'PiB': ur.pebibyte,
            'EiB': ur.exbibyte,
            }

unit_map_inverse = {v: k for k, v in unit_map.items()}
