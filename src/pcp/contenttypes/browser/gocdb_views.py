from Products.Five.browser import BrowserView

header =  """<?xml version="1.0" encoding="UTF-8"?>
<results>"""

footer = """</results>"""

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
