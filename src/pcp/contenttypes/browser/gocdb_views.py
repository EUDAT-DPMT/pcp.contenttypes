from Products.Five.browser import BrowserView

header =  """<?xml version="1.0" encoding="UTF-8"?>
<results>"""

footer = """</results>"""

provider_list_template = """
  <SITE ID="{creg_id}" PRIMARY_KEY="{pk}" NAME="{id}" COUNTRY="{country}" COUNTRY_CODE="? XX ?" ROC="EUDAT_REGISTRY" SUBGRID="" GIIS_URL=""/>"""

provider_template = """
  <SITE ID="{creg_id}" PRIMARY_KEY="{pk}" NAME="{id}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <SHORT_NAME>{id}</SHORT_NAME>
    <OFFICIAL_NAME>{description}</OFFICIAL_NAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <HOME_URL>{url}</HOME_URL>
    <CONTACT_EMAIL>eudat-support@bsc.es</CONTACT_EMAIL>
    <CONTACT_TEL>+34 934 054 221</CONTACT_TEL>
    <COUNTRY_CODE>XX</COUNTRY_CODE>
    <COUNTRY>{country}</COUNTRY>
    <ROC>EUDAT_REGISTRY</ROC>
    <PRODUCTION_INFRASTRUCTURE>{infrastructure}</PRODUCTION_INFRASTRUCTURE>
    <CERTIFICATION_STATUS>Candidate</CERTIFICATION_STATUS>
    <TIMEZONE>{timezone}</TIMEZONE>
    <LATITUDE>{latitude}</LATITUDE>
    <LONGITUDE>{longitude}</LONGITUDE>
    <CSIRT_EMAIL>eudat-security@bsc.es</CSIRT_EMAIL>
    <DOMAIN>
      <DOMAIN_NAME>{domain}</DOMAIN_NAME>
    </DOMAIN>
    <EXTENSIONS>
      <EXTENSION>
        <LOCAL_ID>182</LOCAL_ID>
        <KEY>type</KEY>
        <VALUE>generic</VALUE>
      </EXTENSION>
    </EXTENSIONS>
  </SITE>
"""

service_template = """  
  <SERVICE_ENDPOINT PRIMARY_KEY="{pk}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <HOSTNAME>{hostname}</HOSTNAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <BETA>N</BETA>
    <SERVICE_TYPE>{service_type}</SERVICE_TYPE>
    <HOST_IP>{host_ip}</HOST_IP>
    <CORE></CORE>
    <IN_PRODUCTION>Y</IN_PRODUCTION>
    <NODE_MONITORED>{monitored}</NODE_MONITORED>
    <SITENAME>DKRZ</SITENAME>
    <COUNTRY_NAME>Germany</COUNTRY_NAME>
    <COUNTRY_CODE>DE</COUNTRY_CODE>
    <ROC_NAME>EUDAT_REGISTRY</ROC_NAME>
    <URL>{url}</URL>
    <ENDPOINTS/>
    <EXTENSIONS>
      <EXTENSION>
        <LOCAL_ID>302</LOCAL_ID>
        <KEY>epic_version</KEY>
        <VALUE>2.3</VALUE>
      </EXTENSION>
      <EXTENSION>
        <LOCAL_ID>301</LOCAL_ID>
        <KEY>handle_version</KEY>
        <VALUE>7.3.1</VALUE>
      </EXTENSION>
    </EXTENSIONS>
  </SERVICE_ENDPOINT>
"""

class ProviderView(BrowserView):
    """Render a provider info like GOCDB does."""

    def collect_data(self, context=None):
        """Helper to ccollect the values to be rendered as XML"""
        if context is None:
            context = self.context
        result = {}
        result['id'] = context.Title()
        result['description'] = context.Description()
        result['creg_id'] = context.getCregId()
        result['pk'] = '??? what to use here ???'
        result['dpmt_url'] = context.absolute_url()
        result['creg_url'] = context.getCregURL(url_only=True)
        result['url'] = context.getUrl()
        result['country'] = context.getAddress().get('country','not set')
        result['infrastructure'] = context.getInfrastructure()
        result['timezone'] = context.getTimezone()
        result['latitude'] = context.getLatitude()
        result['longitude'] = context.getLongitude()
        result['domain'] = context.getDomain()
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
        """Helper to ccollect the values to be rendered as XML"""
        context = self.context
        result = {}
        result['id'] = context.Title()
        result['description'] = context.Description()
        result['creg_id'] = context.getCregId()
        result['pk'] = "??? can we use our uid here ???"
        result['dpmt_url'] = context.absolute_url()
        result['creg_url'] = context.getCregURL()
        result['service_type'] = context.getService_type()
        result['host_ip'] = context.getHost_ip4()
        result['monitored'] = context.getMonitored()
        result['url'] = context.getService_url()
        result['hostname'] = context.getHost_name()
        return result

    def xml(self, core=False, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = service_template.format(**data)
        if core:
            return body
        full = header + body + footer
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full
