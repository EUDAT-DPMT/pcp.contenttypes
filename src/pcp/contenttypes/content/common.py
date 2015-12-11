"""Common components shared by content types
"""

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

CommonFields = atapi.Schema((
    atapi.ComputedField('uid',
                        expression="here.UID()",
                         widget=atapi.StringWidget(condition="python:here.stateNotIn(['considered'])"),
                        ),
    atapi.ComputedField('pid',
                        expression="here.PID()",
                        widget=atapi.StringWidget(condition="python:here.stateNotIn(['considered'])"),
                        ),
    ateapi.RecordsField('identifiers',
                        searchable=1,
                        index_method='ids',
                        required=0,
                        subfields = ('type', 'value'),
                        subfield_labels ={'type':'Identifier'},
                        subfield_vocabularies = {'type':'identifierTypes'},
                        innerJoin = ': ',
                        outerJoin = '<br />',
                        widget=ateapi.RecordsWidget(
                            description = "Other types of identifiers used "\
                            "to refer to this item.",
                            label = u"Identifiers",
                            condition="python:here.stateNotIn(['considered'])",
                            ),
    ),
    ateapi.RecordsField('additional',
                        subfields = ('key', 'value'),
                        minimalSize=3,
                        subfield_sizes={'key': 15,
                                        },
                        innerJoin = ': ',
                        outerJoin = '<br />',
                        widget=ateapi.RecordsWidget(
                            description="Other key-value pairs to characterise "\
                            "this item: to be specically used to signal additional information "\
                            "not included in the previous fields.",
                            condition="python:here.stateNotIn(['considered'])",
                            ),
                        ),
    atapi.TextField('text',
                    required=False,
                    searchable=True,
                    primary=True,
                    storage=atapi.AnnotationStorage(migrate=True),
                    validators=('isTidyHtmlWithCleanup',),
                    default_output_type='text/x-html-safe',
                    widget=atapi.RichWidget(
                        description=u'Any other additional information not '\
                        'covered so far.',
                        label=u'Text',
                        rows=15,
                        ),
    ),
))

ResourceFields = atapi.Schema((
    ateapi.RecordsField('compute_resources',
                        required=0,
                        minimalSize=2,
                        subfields = ('cpus', 'memory', 'disk', 
                                     'virtualization', 'software'),
                        subfield_types = {'virtualization': 'selection'},
                        subfield_labels ={'cpus':'CPUs',
                                          'virtualization':'virtualization OK?',
                                          'software':'requires OS/software',
                                          },
                        subfield_vocabularies = {'virtualization': 'yesno'},
                        widget=ateapi.RecordsWidget(label='Compute resources'),
                        ),
    ateapi.RecordsField('storage_resources',
                        required=0,
                        minimalSize=2,
                        subfields = ('size', 'type'),
                        subfield_vocabularies = {'type':'storageTypes'},
                        widget=ateapi.RecordsWidget(label='Storage resources'),
                        ),

))

class CommonUtilities(object):
    """Mixin class to provide shared functionality across content types"""

    def identifierTypes(self, instance):
        """Controlled vocabulary for the supported PID systems"""

        return ateapi.getDisplayList(instance, 'identifier_types', add_select=True)

    def ids(self):
        """Tuple of all identifiers - from the field plus uid and pid"""
        ids = [entry.get('value','') for entry in self.getIdentifiers()]
        ids.append(self.UID())
        handle = self.handle_client._getHandle(self)
        if handle is not None:
            ids.append(handle)
        return tuple(ids)

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
        return self.handle_client._getHandle(self)

    def convert(self, raw):
        """Checking REQUEST for a target unit and converting
        if necessary"""
        
        v = raw.get('value','')
        u = raw.get('unit','')
        result = {'value': v,
                  'unit': u,
                  }
        
        request = self.REQUEST
        try:
            target_unit = request['unit'] 
            if target_unit != u:
                result = self.pint_convert(v, u, target_unit)
        except KeyError:
            pass # no target unit specified
        
        raw.update(result)
        return raw

        
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

    def informationUnits(self, instance=None):
        """
        Controlled vocabulary (DisplayList) of information units 
        supported
        """
        units = unit_map.keys()
        units.sort()
        return atapi.DisplayList(zip(units, units))

    # helper methods for resource handling
    def storageTypes(self, instance):
        """Look up the controlled vocabulary for the storage types
        from the properties tool"""
        
        return ateapi.getDisplayList(instance, 'storage_types', add_select=True)

    def yesno(self, instance):
        """Seems like RecordsFields do not support checkboxes"""
        return atapi.DisplayList([['', 'Select'], ['yes', 'yes'], ['no', 'no']])

# we don't want to use eval so we define an explicit mapping of supported units

from pint import UnitRegistry
ur = UnitRegistry()

unit_map = {'bit': ur.bit,
            'byte':ur.byte,
            'B':   ur.byte,
            'kB':  ur.kilobyte,
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
