from DateTime import DateTime
from incf.countryutils.datatypes import Country
from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from Products.CMFCore.MemberDataTool import MemberData
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import plone


header =  """<?xml version="1.0" encoding="UTF-8"?>
<results>"""

footer = """</results>"""

provider_list_template = """
  <SITE ID="{id}" PRIMARY_KEY="{pk}" NAME="{id_upper}" COUNTRY="{country}" COUNTRY_CODE="{country_code}" ROC="EUDAT_REGISTRY" SUBGRID="" GIIS_URL=""/>"""

extension_template = """
      <EXTENSION>
        <LOCAL_ID>undefined</LOCAL_ID>
        <KEY>{key}</KEY>
        <VALUE>{value}</VALUE>
      </EXTENSION>"""

provider_template = """
  <SITE ID="{id}" PRIMARY_KEY="{pk}" NAME="{id_upper}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <SHORT_NAME>{id_upper}</SHORT_NAME>
    <OFFICIAL_NAME>{description}</OFFICIAL_NAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <HOME_URL>{url}</HOME_URL>
    <CONTACT_EMAIL>{contact_email}</CONTACT_EMAIL>
    <CONTACT_TEL>{contact_tel}</CONTACT_TEL>
    <COUNTRY_CODE>{country_code}</COUNTRY_CODE>
    <COUNTRY>{country}</COUNTRY>
    <ROC>EUDAT_REGISTRY</ROC>
    <PRODUCTION_INFRASTRUCTURE>{infrastructure}</PRODUCTION_INFRASTRUCTURE>
    <CERTIFICATION_STATUS>Candidate</CERTIFICATION_STATUS>
    <TIMEZONE>{timezone}</TIMEZONE>
    <LATITUDE>{latitude}</LATITUDE>
    <LONGITUDE>{longitude}</LONGITUDE>
    <CSIRT_EMAIL>{csirt_email}</CSIRT_EMAIL>
    <DOMAIN>
      <DOMAIN_NAME>{domain}</DOMAIN_NAME>
    </DOMAIN>
{extensions}
  </SITE>
"""

service_template = """  
  <SERVICE_ENDPOINT PRIMARY_KEY="{pk}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <HOSTNAME>{hostname}</HOSTNAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <BETA></BETA>
    <SERVICE_TYPE>{service_type}</SERVICE_TYPE>
    <HOST_IP>{host_ip}</HOST_IP>
    <CORE></CORE>
    <IN_PRODUCTION></IN_PRODUCTION>
    <NODE_MONITORED>{monitored}</NODE_MONITORED>
    <CONTACT_EMAIL>{email}</CONTACT_EMAIL>
    <SITENAME>{site_name}</SITENAME>
    <COUNTRY_NAME>{country}</COUNTRY_NAME>
    <COUNTRY_CODE>{country_code}</COUNTRY_CODE>
    <ROC_NAME>EUDAT_REGISTRY</ROC_NAME>
    <URL>{url}</URL>
    <ENDPOINTS/>
{extensions}
  </SERVICE_ENDPOINT>
"""

term_template = """
  <SERVICE_TYPE TYPE_ID="{id}G0" PRIMARY_KEY="{id}G0">
    <SERVICE_TYPE_NAME>{title}</SERVICE_TYPE_NAME>
    <SERVICE_TYPE_DESC>{description}</SERVICE_TYPE_DESC>
  </SERVICE_TYPE>
"""

service_group_template = """
  <SERVICE_GROUP PRIMARY_KEY="{pk}">
    <NAME>{title}</NAME>
    <DESCRIPTION>{description}</DESCRIPTION>
    <MONITORED>{monitored}</MONITORED>
    <CONTACT_EMAIL>{email}</CONTACT_EMAIL>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    {endpoints}
    <SCOPES>
      <SCOPE>EUDAT</SCOPE>
    </SCOPES>
    <EXTENSIONS/>
  </SERVICE_GROUP>
"""

# helper methods


def getExtensions(data):
    """data holds the list of additional properties as key/value pairs"""
    if not data:
        return ''
    result = ['    <EXTENSIONS>']
    for d in data:
        if not 'key' in d:
            continue
        if not 'value' in d:
            d['value'] = ''
        ext = extension_template.format(**d)
        result.append(ext)
    result.append('    </EXTENSIONS>')
    return "\n".join(result)


def addState(context, data):
    """Add review state to list of additional key/value pairs"""
    state = context.portal_workflow.getInfoFor(context, 'review_state')
    data.append({'key':'state', 'value':state})
    return data


class ProviderView(BrowserView):
    """Render a provider info like GOCDB does."""

    def collect_data(self, context=None):
        """Helper to ccollect the values to be rendered as XML"""
        if context is None:
            context = self.context
        result = {}
        result['id'] = context.getId()
        result['id_upper'] = context.getId().upper()
        result['description'] = context.Description()
        try:
            result['creg_id'] = context.getCregId()
        except KeyError:
            result['creg_id'] = None
        result['pk'] = context.UID()
        result['dpmt_url'] = context.absolute_url()
        try:
            result['creg_url'] = context.getCregURL(url_only=True)
        except KeyError:
            result['creg_url'] = ""
        result['url'] = context.getUrl()
        country = context.getAddress().get('country', 'not set')
        if country == 'not set':
            result['country_code'] = 'not set'
        elif country == 'United Kingdom':
            result['country_code'] = 'UK'
        else:
            result['country_code'] = Country(country).alpha2
        result['country'] = country
        result['infrastructure'] = context.getInfrastructure()
        result['timezone'] = context.getTimezone()
        result['latitude'] = context.getLatitude()
        result['longitude'] = context.getLongitude()
        result['domain'] = context.getDomain()
        contact = context.getContact()
        try:
            result['contact_email'] = contact.getEmail()
        except AttributeError:
            result['contact_email'] = 'not set'
            result['contact_tel'] = 'not set'
        try:
            result['contact_tel'] = contact.getPhone()[0]['number']
        except (AttributeError, IndexError, KeyError):
            result['contact_tel'] = 'not set'
        try:
            result['csirt_email'] = context.getSecurity_contact().getEmail()
        except AttributeError:
            result['csirt_email'] = 'not set'
        additional = context.getAdditional()
        addState(context, additional)
        if additional:
            result['extensions'] = getExtensions(additional)
        else:
            result['extensions'] = '<EXTENSIONS/>'
        #result[''] = 1
        return result

    def xml(self, core=False, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = provider_template.format(**data)
        body = body.replace('&', '&amp;')
        if core:
            return body
        full = header + body + footer
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full

    def get_site_list(self):
        """XML formatted listing of providers"""
        context = self.context
        sites = context.portal_catalog(portal_type='Provider')
        bodies = []
        for site in sites:
            data = self.collect_data(context=site.getObject())
            body = provider_list_template.format(**data)
            bodies.append(body)
        body = ''.join(bodies)
        body = body.replace('&', '&amp;')
        full = header + body + footer
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full


class ServiceView(BrowserView):
    """Render a registered service component info like GOCDB does."""

    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        result = {}
        result['id'] = context.Title()
        result['description'] = context.Description()
        result['creg_id'] = context.getCregId()
        result['pk'] = context.UID()
        result['dpmt_url'] = context.absolute_url()
        result['creg_url'] = context.getCregURL(url_only=True)
        # the following ought to be simpler but it seems to work anyway
        result['service_type'] = context.Schema()['service_type'].vocabulary.getVocabularyDict(context).get(context.getService_type(),'')
        result['host_ip'] = context.getHost_ip4()
        result['monitored'] = context.getMonitored()
        contacts = context.getContacts()
        result['email'] = ','.join([contact.getEmail() for 
                                    contact in contacts])
        result['url'] = context.getService_url()
        result['hostname'] = context.getHost_name()
        # the below assumes that our acquisition parent is a provider
        result['site_name'] = context.aq_parent.getId().upper()
        country = context.aq_parent.getAddress().get('country', 'not set')
        if country == 'not set':
            result['country_code'] = 'not set'
        elif country == 'United Kingdom':
            result['country_code'] = 'UK'
        else:
            result['country_code'] = Country(country).alpha2
        result['country'] = country
        additional = context.getAdditional()
        addState(context, additional)
        if additional:
            result['extensions'] = getExtensions(additional)
        else:
            result['extensions'] = '<EXTENSIONS/>'
        return result

    def xml(self, core=False, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = service_template.format(**data)
        if core:
            return body
        full = header + body + footer
        full = full.replace('&', '&amp;')
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full

class ServiceGroupView(BrowserView):
    """Render a registered service info like GOCDB does."""

    def getEndpoints(self):
        """Render related registered service components"""
        context = self.context
        result = []
        for rsc in context.getService_components():
            result.append(rsc.restrictedTraverse('xml').xml(core=True))
        return '\n'.join(result)

    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        result = {}
        result['id'] = context.getId()
        result['title'] = context.Title()
        result['description'] = context.Description()
        result['creg_id'] = context.getCregId()
        result['pk'] = context.UID()
        result['dpmt_url'] = context.absolute_url()
        result['creg_url'] = context.getCregURL(url_only=True)
        result['monitored'] = context.getMonitored()
        contact = context.getContact()
        if contact is not None:
            result['email'] = contact.getEmail()
        else:
            result['email'] = '(no contact information available)'
        result['endpoints'] = self.getEndpoints()
        additional = context.getAdditional()
        addState(context, additional)
        if additional:
            result['extensions'] = getExtensions(additional)
        else:
            result['extensions'] = '<EXTENSIONS/>'
        return result

    def xml(self, core=False, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = service_group_template.format(**data)
        if core:
            return body
        full = header + body + footer
        full = full.replace('&', '&amp;')
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full


class TermView(BrowserView):
    """Render a simple vocabulary term info like GOCDB does.
       This is needed for teh service types.
    """

    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        result = {}
        result['id'] = context.getId()
        result['title'] = context.Title()
        result['description'] = context.Description()
        return result

    def xml(self, core=False, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = term_template.format(**data)
        if core:
            return body
        full = header + body + footer
        full = full.replace('&', '&amp;')
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full


class DowntimeView(BrowserView):

    def secsSinceEpoch(self, datetime):
        return datetime.millis() / 1000

    def effectiveDate(self, downtime):
        return downtime.getEffectiveDate() or downtime.created()

    def getHosters(self, registeredComponent):
        return ','.join([x.Title() if x else '?' for x in registeredComponent.getService_providers()])

    def getServiceType(self, component):
        serviceType = component.getService_type()
        vocabulary = getUtility(IVocabularyFactory, 'dpmt.service_types')
        vocabulary = vocabulary(component)
        return vocabulary.by_value[serviceType]

    def buildDateRangeQuery(self, min, max):
        if min or max:
            if max:
                max += 1
            if min and max:
                return dict(query=(min, max), range='min:max')
            else:
                return dict(query=min or max, range=(min and 'min') or (max and 'max'))
        return None

    def getDowntimes(self):
        query = dict()

        query['portal_type'] = 'Downtime'
        query['review_state'] = 'published'

        # TODO: use AdvancedQuery or merge date and window manually
        start_min, start_max = None, None
        end_min, end_max = None, None

        startdate = self.request.form.get('startdate', None)
        startdate = DateTime(startdate) if startdate else None
        if startdate:
            start_min = startdate  # query['start'] = dict(query=startdate, range='min')

        enddate = self.request.form.get('enddate', None)
        enddate = DateTime(enddate) if enddate else None
        if enddate:
            end_max = enddate  # query['end'] = dict(query=enddate+1, range='max')

        windowstart = self.request.form.get('windowstart', None)
        windowstart = DateTime(windowstart) if windowstart else None
        if windowstart:
            end_min = windowstart  # query['end'] = dict(query=windowstart, range='min')

        windowend = self.request.form.get('windowend', None)
        windowend = DateTime(windowend) if windowend else None
        if windowstart:
            start_max = windowend  # query['start'] = dict(query=windowend+1, range='max')

        ongoing_only = self.request.form.get('ongoing_only', 'no')
        if ongoing_only == 'yes':
            now = DateTime()
            start_max = min(now, start_max) if start_max else now
            end_min = min(now, end_min) if end_min else now

        if start_min or start_max:
            query['start'] = self.buildDateRangeQuery(start_min, start_max)
        if end_min or end_max:
            query['end'] = self.buildDateRangeQuery(end_min, end_max)

        catalog = self.context.portal_catalog
        downtime_brains = catalog(query)

        return [brain.getObject() for brain in downtime_brains]

    def getEndpoints(self, downtime):
        endpoints = set()
        for affected in downtime.getAffected_registered_serivces():
            if IRegisteredService.providedBy(affected):
                # all endpoints of the affected service are therefore affected, too
                service = affected
                endpoints.update(service.getService_components())

            if IRegisteredServiceComponent.providedBy(affected):
                # get service of affected endpoint
                # services = affected.getParent_services()
                endpoints.update((affected,))

        return endpoints


class SiteContactsView(BrowserView):

    def getSites(self):
        query = dict(
            portal_type='Provider',
        )

        sitename = self.request.form.get('sitename', None)
        if sitename:
            query['Title'] = sitename

        catalog = self.context.portal_catalog
        return [brain.getObject() for brain in catalog(query)]

    def getSiteContacts(self, site):
        roletype = self.request.get('roletype', None)
        allowed_roles = ('Administrator', 'Can review', 'CDI Manager', 'CDI Member', 'Customer Relationship Manager',
                         'Enabler', 'Principal', 'Project Manager', 'Site Manager',)

        if roletype:
            allowed_roles = (roletype,) if roletype in allowed_roles else ()

        def filter_roles(rs):
            return [r for r in rs if r in allowed_roles]

        return [(plone.api.user.get(userid=userid), filter_roles(roles)) for userid, roles in site.get_local_roles()]

