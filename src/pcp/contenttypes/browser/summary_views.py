import plone.api
from datetime import datetime
from cStringIO import StringIO
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import ReferenceField

CSV_TEMPLATE = '"%s"'

# helper functions to render not so simple fields


def render_state(content, field_id):
    return content.portal_workflow.getInfoFor(content, 'review_state')


def render_type(content, field_id):
    ti = content.getTypeInfo()
    return ti.Title()


def render_reference_field(content, field_id):
    field = content.schema[field_id]
    objs = field.get(content, aslist=True)
    text = []
    if objs == []:
        return "no reference set"
    for item in objs:
        text.append("<a href='%s'>%s</a>" %
                    (item.absolute_url(), item.Title()))
    return "<br />".join(text)


def render_with_link(content, field_id):
    field = content.schema[field_id]
    value = field.get(content)
    url = content.absolute_url()
    return "<a href='%s'>%s</a>" % (url, value)


def render_parent(content, field_id):
    parent = content.aq_inner.aq_parent
    title = parent.Title()
    url = parent.absolute_url()
    return "<a href='%s'>%s</a>" % (url, title)


def modification_date(content, field_id):
    value = content.modified()
    return value.Date()


def render_date(content, field_id):
    field = content.schema[field_id]
    value = field.get(content)
    try:
        return value.Date()
    except AttributeError:
        return 'not set'


def render_resources(content, field_id):
    """Specific for requests"""
    try:
        return content.request_details()
    except AttributeError:
        return 'none specified'


class BaseSummaryView(BrowserView):
    """Base class for various summary views"""

    render_methods = {'state': render_state,
                      'portal_type': render_type,
                      'title': render_with_link,
                      'parent_provider': render_parent,
                      'parent_project': render_parent,
                      'modified': modification_date,
                      'startDate': render_date,
                      'resources': render_resources,
                      # add more as needed; reference fields don't need to be
                      # included here
                      }

    def field_visible(self, obj, field_name):

        field = obj.getField(field_name)
        if field:
            permission = field.read_permission
            return plone.api.user.has_permission(
                permission=permission,
                user=plone.api.user.get_current(),
                obj=obj)
        return True

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def workflow_tool(self):
        return getToolByName(self.context, 'portal_workflow')

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title',

                #                'services_used',
                'allocated', 'used', 'community',
                'topics', 'start_date', 'end_date', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title',
                #                'Service',
                'Allocated storage', 'Used storage',
                'Customer', 'Topics',
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


class CustomerOverview(BaseSummaryView):
    """Overview of all customers/sponsors/communities"""

    title = "EUDAT Customers"

    description = "All current and past EUDAT customers/sponsors/communities"

    def content_items(self):
        """All customers regardless of location"""
        # customers were originally called communities
        return [element.getObject() for element in self.catalog(portal_type='Community')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'topics', 'representative', 'projects_involved', 'primary_provider',
                'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Topics', 'Representative', 'Projects', 'Provider',
                'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('topics',)


class ProviderOverview(BaseSummaryView):
    """Overview of all providers of EUDAT services"""

    title = "EUDAT Provider"

    description = "All current and past providers of EUDAT services"

    def content_items(self):
        """All providers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Provider')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'url', 'contact', 'provider_type', 'provider_status', 'alarm_email', 'helpdesk_email',
                'modified')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Website', 'Contact', 'Type', 'Status', 'Alarm email', 'Helpdesk email',
                'Modified')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('url', 'alarm_email', 'helpdesk_email', 'provider_status', 'provider_type')


class ServiceOverview(BaseSummaryView):
    """Overview of all EUDAT services"""

    title = "EUDAT Catalog"

    description = "All current and past EUDAT services"

    def content_items(self):
        """All services regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Service', path='/pcp/catalog')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'service_type', 'service_owner', 'contact',
                'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Type', 'Owner', 'Contact',
                'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('service_type',)


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


class RequestOverview(BaseSummaryView):
    """Overview of all requests no matter what type or state or where they are located"""

    title = "All Requests"

    description = "All requests across the entire site."

    def content_items(self):
        """All requests regardless of location"""
        types = ['ServiceRequest', 'ServiceComponentRequest', 'ResourceRequest']
        return [element.getObject() for element in self.catalog(portal_type=types)]

    def fields(self):
        """hardcoded for a starts"""
        return ('parent_project', 'portal_type', 'title', 'resources', 'startDate',
                'preferred_providers', 'state')

    def field_labels(self):
        """Hardcoded label"""
        return ('Requesting Project', 'Request Type', 'Request Title', 'Requested Resources',
                'Requested Start Date', 'Preferred Provider(s)', 'State')


class ApprovedRequests(RequestOverview):
    """All approved but unfulfilled requests"""

    title = "Approved Requests"

    description = "All appoved but unfulfilled requests, i.e., those that need to be acted upon"

    def content_items(self):
        """All approved requests regardless of location"""
        types = ['ServiceRequest', 'ServiceComponentRequest', 'ResourceRequest']
        return [element.getObject() for element in
                self.catalog(portal_type=types, review_state='approved')]


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
                if isinstance(text, unicode):
                    text = text.encode('utf8')
                value = CSV_TEMPLATE % text
                values.append(value)
            out.write(delimiter.join(values) + newline)

        value = out.getvalue()
        out.close()

        timestamp = datetime.today().strftime("%Y%m%d%H%M")
        filename = filenamebase + timestamp + '.csv'

        self.request.RESPONSE.setHeader(
            'Content-Type', 'application/x-msexcel')
        self.request.RESPONSE.setHeader("Content-Disposition",
                                        "inline;filename=%s" % filename)

        return value
