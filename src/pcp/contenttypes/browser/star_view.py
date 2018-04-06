# provide a StAR (Storage Accounting Record) view for 
# Registered Storage Components
# For specification see: http://cds.cern.ch/record/1452920/files/GFD.201.pdf

import time
from datetime import datetime, timedelta

from pcp.contenttypes.browser.accounting import Accounting

minimal_star_template = """
<sr:StorageUsageRecord
 xmlns:sr="http://eu-emi.eu/namespaces/2011/02/storagerecord">
  <sr:RecordIdentity sr:createTime="{endtime}Z"
                     sr:recordId="accounting.eudat.eu/eudat/{rsr_id}/{record_id}"/>
  <sr:StorageSystem>{url}</sr:StorageSystem>
  <sr:StartTime>{starttime}Z</sr:StartTime>
  <sr:EndTime>{endtime}Z</sr:EndTime>
  <sr:ResourceCapacityUsed>{usage}</sr:ResourceCapacityUsed>
</sr:StorageUsageRecord>
"""

class StarView(Accounting):
    """Render a StAR view for registered storage components"""
    
    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        records = self.records()
        if records:
            latest = records[0]
        else:
            latest = {'core': {'value': 0, 'unit': 'byte'}, 
                      'meta': {ts: time.time()}}

        result = {}
        result['id'] = context.getId()
        result['title'] = context.Title()
        result['description'] = context.Description()
        result['url'] = context.absolute_url()
        result['rsr_id'] = context.UID()
        result['record_id'] = latest['meta'].get('ts')
        ts = latest['meta'].get('ts')
        endtime = datetime.utcfromtimestamp(ts)
        result['endtime'] = endtime.isoformat()
        result['starttime'] = (endtime - timedelta(days=1)).isoformat()
        # this should be in byte without unit
        result['usage'] = ' '.join([latest['core'].get('value'), 
                                    latest['core'].get('unit')])
        return result

    def star(self):
        """Render info using template"""
        data = self.collect_data()
        body = minimal_star_template.format(**data)
        full = body.replace('&', '&amp;')
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full
