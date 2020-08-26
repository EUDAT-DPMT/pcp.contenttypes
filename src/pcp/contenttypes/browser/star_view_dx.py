# provide a StAR (Storage Accounting Record) view for 
# Registered Storage Components
# For specification see: http://cds.cern.ch/record/1452920/files/GFD.201.pdf

import time
from datetime import datetime, timedelta

from pcp.contenttypes.browser.accounting import Accounting

single_star_template = """<sr:StorageUsageRecord{}
</sr:StorageUsageRecord>
"""

multiple_star_template = """
<sr:StorageUsageRecords
 xmlns:sr="http://eu-emi.eu/namespaces/2011/02/storagerecord">
 {}</sr:StorageUsageRecords>
"""

body_star_template = \
"""{ns}  
  <sr:RecordIdentity sr:createTime="{endtime}Z"
                     sr:recordId="accounting.eudat.eu/eudat/{rsr_id}/{record_id}"/>
  <sr:Site>EUDAT-{site}</sr:Site>
  <sr:StorageSystem>{url}</sr:StorageSystem>
  <sr:StartTime>{starttime}Z</sr:StartTime>
  <sr:EndTime>{endtime}Z</sr:EndTime>
  <sr:ResourceCapacityUsed>{usage}</sr:ResourceCapacityUsed>
  <sr:SubjectIdentity>
    <sr:LocalUser>{customer_title}</sr:LocalUser>
    <sr:LocalGroup>{project_title}</sr:LocalGroup>
    <sr:UserIdentity>{customer_url}</sr:UserIdentity>
    <sr:Group>{project_url}</sr:Group>
    <sr:GroupAttribute sr:attributeType='title'>{project_title}</sr:GroupAttribute>
    <sr:GroupAttribute sr:attributeType='scope'>{project_scope}</sr:GroupAttribute>
  </sr:SubjectIdentity>"""

class StarView(Accounting):
    """Render a StAR view for registered storage components"""
    
    def collect_data(self):
        """Helper to collect the values to be rendered as XML"""
        context = self.context
        records = self.records()
        if records:
            latest = records[0]
            if latest['core'].get('unit') not in ['B', 'byte', 'Byte']:
                raw = latest['core'].copy()
                normalized = context.convert_pure(raw, 'byte')
                # turning stuff like '6.92e+14' into '692000000000000'
                normalized['value'] = str(int(float(normalized['value'])))
                latest['core'].update(normalized)
        else:
            latest = {'core': {'value': '0', 'unit': 'byte'}, 
                      'meta': {'ts': time.time()}}

        result = {}
        result['ns'] = ''
        result['id'] = context.getId()
        result['id_upper'] = context.getId().upper()
        result['title'] = context.Title()
        result['description'] = context.Description()
        result['url'] = context.absolute_url()
        result['rsr_id'] = context.UID()
        result['record_id'] = latest['meta'].get('ts')
        ts = latest['meta'].get('ts')
        endtime = datetime.utcfromtimestamp(ts)
        result['endtime'] = endtime.isoformat()
        result['starttime'] = (endtime - timedelta(days=1)).isoformat()
        result['usage'] = latest['core'].get('value')  # has to be in byte
        # the below assumes that our acquisition parent is a provider
        result['site'] = context.aq_parent.getId().upper()
        customer = context.customer.to_object
        if customer is None: 
            result['customer_title'] = "(no customer found)"
            result['customer_url'] = "(no customer found)"
        else: 
            result['customer_title'] = customer.Title().decode('utf-8').encode('ascii', 'xmlcharrefreplace')
            result['customer_url'] = customer.absolute_url()
        project = context.project.to_object
        if project is None:
            result['project_title'] = "(no project found)"
            result['project_url'] = "(no project foumd)"
        else:
            result['project_title'] = project.Title().decode('utf-8').encode('ascii', 'xmlcharrefreplace')
            result['project_url'] = project.absolute_url()
        result['project_scope'] = context.getScopeValues(asString=1) or "EUDAT"
        return result

    def star(self, with_ns=True):
        """Render info using template"""
        data = self.collect_data()
        if with_ns:
            data['ns'] = '\n  xmlns:sr="http://eu-emi.eu/namespaces/2011/02/storagerecord">'
        else:
            data['ns'] = '>'
        body = body_star_template.format(**data)
        body = body.replace('&', '&amp;')
        full = single_star_template.format(body)
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full

class RecordsView(StarView):
    """Render a StAR view for all registered storage components"""
    
    def all_rsr(self):
        """All registered storage resources"""
        catalog = self.context.portal_catalog
        brains = catalog(portal_type=['registeredstorageresource_dx'])
        objects = [b.getObject() for b in brains]
        return objects

    def records(self):
        """XML body of the records listing"""
        objects = self.all_rsr()
        result = []
        for o in objects:
            record = o.unrestrictedTraverse('@@star')(with_ns=False)
            result.append(record)
        return ''.join(result)
    
    def star(self):
        body = self.records()
        full = multiple_star_template.format(body)
        self.request.response.setHeader('Content-Type', 'text/xml')
        return full
        

