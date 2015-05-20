from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField


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
        return ('title', 'services_used', 'service_provider', 'resources', 'community', 'topics', 'start_date', 'state')

    def field_labels(self):
        """hardcoded for a start"""
        return ('Title', 'Service', 'Service provider', 'Resources', 'Community', 'Topics', 'Start date', 'State')

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
                    value['text'] = obj.Title()
                    value['url'] = obj.absolute_url()
                elif field == 'title':
                    value['text'] = f.get(project)
                    value['url'] = project.absolute_url()
                elif field == 'start_date':
                    value['text'] = f.get(project).Date()
                    value['url'] = None 
                elif field == 'resources':
                    data = f.get(project)
                    values = []
                    for k, v in data.items():
                         values.append('%s: %s' % (k, v))
                    value['text'] = '<br />'.join(values)
                    value['url'] = None
                else:
                    value['text'] = f.get(project)
                    value['url'] = None 
                result.append(value)
            results.append(result)

        return results
