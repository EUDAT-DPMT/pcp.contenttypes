# provide a StAR (Storage Accounting Record) view for 
# Registered Storage Components
# For specification see: http://cds.cern.ch/record/1452920/files/GFD.201.pdf

from Products.Five.browser import BrowserView

minimal_star_template = """
<sr:StorageUsageRecord
 xmlns:sr="http://eu-emi.eu/namespaces/2011/02/storagerecord">
  <sr:RecordIdentity sr:createTime="2010-11-09T09:06:52Z"
                     sr:recordId="host.example.org/sr/87912469269276"/>
  <sr:StorageSystem>host.example.org</sr:StorageSystem>
  <sr:StartTime>2010-10-11T09:31:40Z</sr:StartTime>
  <sr:EndTime>2010-10-12T09:29:42Z</sr:EndTime>
  <sr:ResourceCapacityUsed>13617</sr:ResourceCapacityUsed>
</sr:StorageUsageRecord>
"""

class StarView(BrowserView):
    """Render a StAR view for registered storage components"""

    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        result = {}
        result['id'] = context.getId()
        result['title'] = context.Title()
        result['description'] = context.Description()
        return result

    def star(self):
        """Render info using template"""
        data = self.collect_data()
        body = minimal_star_template.format(**data)
        full = body.replace('&', '&amp;')
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full
