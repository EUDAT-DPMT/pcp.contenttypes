from types import UnicodeType
from datetime import datetime
from StringIO import StringIO
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField

CSV_TEMPLATE = '"%s"'


class ProjectOverview(BrowserView):
    """Provide data suitable for the overview template"""

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def workflow_tool(self):
        return getToolByName(self.context, 'portal_workflow')

    def fields(self):
        """hardcoded for a start"""
        return ('title', 'services_used', 'service_provider', 
                'allocated', 'used', 'resources', 'community', 
                'topics', 'start_date', 'state')

    def field_labels(self):
        """hardcoded for a start"""
        return ('Title', 'Service', 'Service provider', 
                'Allocated storage', 'Used storage', 
                'Resources', 'Community', 'Topics', 
                'Start date', 'State')

    def data(self):
        projects = [element.getObject() for element in self.catalog(portal_type='Project')]

        results = []

        for project in projects:
            result = []
            for field in self.fields():
                value = {}
                if field == 'state':
                    value['text'] = self.workflow_tool.getInfoFor(project, 'review_state')
                    value['url'] = None
                    result.append(value)
                    continue
                f = project.schema[field]
                if isinstance(f, ReferenceField):
                    obj = f.get(project)
                    if obj is not None:
                        value['text'] = obj.Title()
                        value['url'] = obj.absolute_url()
                    else:
                        value['text'] = 'no reference set'
                        value['url'] = '.'
                elif field == 'title':
                    value['text'] = f.get(project)
                    value['url'] = project.absolute_url()
                elif field == 'start_date':
                    date = f.get(project)
                    if date is not None:
                        value['text'] = f.get(project).Date()
                        value['url'] = None 
                    else:
                        value['text'] = 'no date set'
                        value['url'] = None    
                elif field == 'resources':
                    data = f.get(project)
                    values = []
                    for k, v in data.items():
                         values.append('%s: %s' % (k, v))
                    value['text'] = '<br />'.join(values)
                    value['url'] = None
                elif field in ['allocated', 'used']:
                    raw = f.getRaw(project)
                    value['text'] = "%s %s" % (raw.get('value', ''), 
                                               raw.get('unit', ''))
                    value['url'] = None                     
                else:
                    value['text'] = f.get(project)
                    value['url'] = None 
                result.append(value)
            results.append(result)

        return results


class CsvView(ProjectOverview):
    """View class for the CSV output of projects"""

    def csv_export(self,
                   states=None,
                   fields=None,
                   filenamebase='projects',
                   delimiter=',',
                   newline='\r\n',
                   ):
        """Main method to be called for the csv export"""
        
        if fields is None:
            fields = self.fields()
            
        out = StringIO()
        out.write(delimiter.join(fields) + newline)

        for project in self.data():
            values = []
            for field in project:
                text = field['text']
                if type(text) is UnicodeType:
                    text = text.encode('utf8')
                value = CSV_TEMPLATE % text
                values.append(value)
            out.write(delimiter.join(values) + newline)
            
        value = out.getvalue()
        out.close()

        timestamp = datetime.today().strftime("%Y%m%d%H%M")
        filename = filenamebase + timestamp + '.csv'
        
        self.request.RESPONSE.setHeader('Content-Type', 'application/x-msexcel')
        self.request.RESPONSE.setHeader("Content-Disposition", 
                                        "inline;filename=%s"%filename)

        return value
