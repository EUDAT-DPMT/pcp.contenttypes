from types import UnicodeType
from datetime import datetime
from StringIO import StringIO
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField

CSV_TEMPLATE = '"%s"'

# helper functions to render not so simple fields
def render_state(content, field_id):
    return content.portal_workflow.getInfoFor(content, 'review_state')

def render_reference_field(content, field_id):
    field = content.schema[field_id]
    objs = field.get(content, aslist=True)
    text = []
    if objs == []:
        return "no reference set"
    for item in objs:
        text.append("<a href='%s'>%s</a>" % (item.absolute_url(), item.Title()))
    return "<br />".join(text)

def render_with_link(content, field_id):
    field = content.schema[field_id]
    value = field.get(content)
    url = content.absolute_url()
    return "<a href='%s'>%s</a>" % (url, value)

def render_parent_provider(content, field_id):
    parent = content.aq_inner.aq_parent
    title = parent.Title()
    url = parent.absolute_url()
    return "<a href='%s'>%s</a>" % (url, title)

class BaseSummaryView(BrowserView):
    """Base class for various summary views"""

    render_methods = {'state':render_state,
                      'title':render_with_link,
                      'parent_provider':render_parent_provider,
                      # add more as needed; reference fields don't need to be included here
    }
        
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def workflow_tool(self):
        return getToolByName(self.context, 'portal_workflow')

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'services_used', 
                'allocated', 'used', 'community', 
                'topics', 'start_date', 'end_date', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Service',  
                'Allocated storage', 'Used storage', 
                'Community', 'Topics', 
                'Start date', 'End date', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('allocated', 'used', 'topics', 'start_date', 'end_date')

    def content_items(self, portal_type):
        """The content items to show"""
        return [element.getObject() for element in self.catalog(portal_type=portal_type)]


    def render(self, content, field_id):
        """Dispatcher for rendering not-so-simple fields"""
        renderer = self.render_methods.get(field_id, render_reference_field)
        return renderer(content, field_id)

class ProjectOverview(BaseSummaryView):
    """Overview of all projects"""
    # almost identical to base class as this is the driving use case 
    # implemented in the base class

    title = "Project Overview"

    description = "All current and past projects"

    def content_items(self):
        """All projects regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Project')]

class RegisteredServiceOverview(BaseSummaryView):
    """Overview of all registered services no matter where they are"""

    title = "Registered Services"

    description = "All registered services across the entire site."

    def content_items(self):
        """All registered services regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='RegisteredService')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'contact', 'managers', 'monitored', 'service_components', 
                'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Contact', 'Manager(s)', 'Monitored', 'Service component(s)',  
                'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('monitored',)

class RegisteredServiceComponentOverview(BaseSummaryView):
    """Overview of all registered services components no matter where they are located"""
    
    title = "Registered Service Components"

    description = "All registered service components across the entire site."

    def content_items(self):
        """All registered service components regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='RegisteredServiceComponent')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'service_url', 'parent_provider', 'contacts', 
                'monitored', 'host_name', 
                'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Title', 'URL', 'Provider', 'Contact(s)', 'Monitored', 'Host name',
                'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('service_url', 'monitored', 'host_name')
    
class RegisteredResourceOverview(BaseSummaryView):
    """Overview of all registered resources no matter where they are located"""
    
    title = "Registered Resources"

    description = "All registered resources across the entire site."

    def content_items(self):
        """All registered resources regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='RegisteredResource')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'parent_provider', 'compute_resources', 'storage_resources',
                'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Title', 'Provider', 'Compute resources', 'Storage resources',
                'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('compute_resources', 'storage_resources')

class ResourceOfferOverview(RegisteredResourceOverview):
    """Overview of all resource offers no matter which provider made them"""
    
    title = "Resource Offers"

    description = "All resource offers from all providers."

    def content_items(self):
        """All resource offers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='ResourceOffer')]



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
