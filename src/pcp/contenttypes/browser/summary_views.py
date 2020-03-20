import plone.api
from datetime import datetime
from cStringIO import StringIO
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_callable
from Products.Archetypes.atapi import ReferenceField

CSV_TEMPLATE = '"%s"'

# helper functions to render not so simple fields


def render_state(content, field_id):
    return content.portal_workflow.getInfoFor(content, 'review_state')


def render_type(content, field_id):
    ti = content.getTypeInfo()
    return ti.Title()


def render_reference_field(content, field_id, with_state=False):
    field = content.schema[field_id]
    objs = field.get(content, aslist=True)
    text = []
    if objs == []:
        return "no reference set"
    for item in objs:
        if with_state:
            state = content.portal_workflow.getInfoFor(item, 'review_state')
            text.append("<a href='%s'>%s</a> (%s)" %
                        (item.absolute_url(), item.Title(), state))

        else:
            text.append("<a href='%s'>%s</a>" %
                        (item.absolute_url(), item.Title()))
    return "<br />".join(text)

def render_service_options(content, field_id, with_state=False):
    try:
        objs = content['options'].contentValues()
    except KeyError:
        return "No options specified"
    text = []
    if objs == []:
        return "no options specified"
    for item in objs:
        if item.portal_type != 'Document':
            # this assumes that all documents here describe options
            # and other types don't
            continue
        if with_state:
            state = content.portal_workflow.getInfoFor(item, 'review_state')
            text.append("<a href='%s'>%s</a> (%s)" %
                        (item.absolute_url(), item.Title(), state))

        else:
            text.append("<a href='%s'>%s</a>" %
                        (item.absolute_url(), item.Title()))
    return "<br />".join(text)

def render_service_components(content, field_id):
    return render_reference_field(content, field_id, with_state=True)


def render_with_link(content, field_id):
    field = content.schema[field_id]
    value = field.get(content)
    url = content.absolute_url()
    return "<a href='%s'>%s</a>" % (url, value)

def render_with_link_dx(content, field_id):
    field_value = getattr(content, field_id, '')
    if safe_callable(field_value):
        field_value = field_value()
    url = content.absolute_url()
    return "<a href='%s'>%s</a>" % (url, field_value)


def render_parent(content, field_id):
    parent = content.aq_inner.aq_parent
    title = parent.Title()
    url = parent.absolute_url()
    return "<a href='%s'>%s</a>" % (url, title)


def render_grandparent(content, field_id):
    parent = content.aq_inner.aq_parent
    grandparent = parent.aq_inner.aq_parent
    title = grandparent.Title()
    url = grandparent.absolute_url()
    return "<a href='%s'>%s</a>" % (url, title)


def creation_date(content, field_id):
    value = content.created()
    return value.Date()


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

def render_number_of_objects(content, field_id):
    """
    Return the number of registered objects.
    Only available for 'Registered Storage Resources'
    """
    try:
        return content.getNumberOfRegisteredObjects()
    except AttributeError:
        return "none"

def render_contact_email(content, field_id):
    """
    Return the email address from the referenced contact object
    """
    try:
        email = content.getContact().getEmail()
    except AttributeError:
        email = ''
    email_link = '<a href="mailto:%s">%s</a>'
    return email_link % (email, email)

def render_business_email(content, field_id):
    """
    Return the email address from the referenced business contact object
    """
    try:
        email = content.getBusiness_contact().getEmail()
    except AttributeError:
        email = ''
    email_link = '<a href="mailto:%s">%s</a>'
    return email_link % (email, email)

def provider_contact_email(content, field_id):
    """
    Look up the parent provider and get to its contact email
    """
    parent = content.aq_inner.aq_parent
    return render_contact_email(parent, '')

def provider_business_email(content, field_id):
    """
    Look up the parent provider and get to its business contact email
    """
    parent = content.aq_inner.aq_parent
    return render_business_email(parent, '')

def render_constraints(content, field_id):
    """
    Return the aggregated constraints
    """
    return content.aggregated_constraints()

class DetailedView(BrowserView):
    """Dispatcher to the more specific summary views"""

    def detailed_view(self):

        id = self.context.getId()
        
        mapping = {
            'projects':'project_summary_view',
            'customers':'customer_overview',
            'providers':'provider_overview',
            'catalog':'service_overview'
        }
        
        view = mapping.get(id, 'folder_summary_view')
        
        target = '{base}/{view}'.format(base=self.context.absolute_url(), 
                                        view=view)
        return self.request.response.redirect(target)



class BaseSummaryView(BrowserView):
    """Base class for various summary views"""

    render_methods_dx = {'title': render_with_link_dx,
                         'parent_rsc': render_parent,     # endpoint specific
                         'provider': render_grandparent,  # endpoint specific
                     }

    render_methods = {'state': render_state,
                      'portal_type': render_type,
                      'title': render_with_link,
                      'parent_provider': render_parent,
                      'parent_project': render_parent,
                      'created': creation_date,
                      'modified': modification_date,
                      'startDate': render_date,
                      'resources': render_resources,
                      'service_options': render_service_options,
                      'service_components': render_service_components,
                      'number': render_number_of_objects,
                      'contact_email': render_contact_email,
                      'business_email': render_business_email,
                      'provider_contact_email': provider_contact_email,
                      'provider_business_email': provider_business_email,
                      'constraints': render_constraints,
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
                'community', 'registered_services_used', 'general_provider',
                'topics', 'scopes', 'used_new', 'registered_objects',
                'start_date', 'end_date', 'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Title',
                'Customer', 'Service(s)', 'General provider',
                'Topics', 'Scope(s)', 'Used Storage', 'Objects',
                'Start date', 'End date', 'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('used_new', 'registered_objects', 'topics', 'scopes', 'start_date', 'end_date')

    def content_items(self, portal_type):
        """The content items to show"""
        return [element.getObject() for element in self.catalog(portal_type=portal_type)]

    def render(self, content, field_id):
        """Dispatcher for rendering not-so-simple fields"""
        renderer = self.render_methods.get(field_id, render_reference_field)
        return renderer(content, field_id)

class EndpointOverview(BaseSummaryView):
    """All specific endpoints"""
    
    title = "Service Endpoints"
    description = "All specific endpoints of services / service components"
 
    def content_items(self):
        """All endpoint entries"""
        etypes = ['endpoint_handle', 'endpoint_irods']
        return [element.getObject() for element in self.catalog(portal_type=etypes)]

    def fields(self):
        """Field names; needs to exist at all endpoint types"""
        return ('title', 'parent_rsc','provider', 'host', 'monitored', 
                'system_operations_user', 'related_project','related_service')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Service endpoint', 'Service component','Provider', 'Host', 'Monitored',
                'System operations user', 'Project','Service')

    def render(self, content, field_id):
        """Dexterity type rendering of field values"""
        # https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/browser/folder.py
        renderer = self.render_methods_dx.get(field_id, None)
        if renderer is not None:
            return renderer(content, field_id)
        value = getattr(content, field_id, '')
        # catch relation fields
        target = getattr(value, 'to_object', None)
        if target is not None:
            title = target.Title()
            url = target.absolute_url()
            return "<a href='%s'>%s</a>" % (url, title)
        if safe_callable(value):
            value = value()

        return value
    

class PeopleOverview(BaseSummaryView):
    """Overview of all people involved"""

    title = "People"

    description = "All people/address book information stored in DPMT"

    def content_items(self):
        """All address book entries"""
        return [element.getObject() for element in self.catalog(portal_type='Person')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'email', 'affiliation', 'manages', 'provider_contact_for', 'business_contact_for', 
               'security_contact_for', 'provider_admin', 'she_contact', 'community_contact_for', 
               'community_representative', 'community_admin', 'enables', 'service_owner_of', 
               'principle_investigator_of','manager_of_registered_service')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classs"""
        return ('title', 'email', 'affiliation', 'manages', 'provider_contact_for', 'business_contact_for',
               'security_contact_for', 'provider_admin', 'she_contact', 'community_contact_for',
               'community_representative', 'community_admin', 'enables', 'service_owner_of',
               'principle_investigator_of','manager_of_registered_service')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ['email']

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
        return ('title', 'topics', 'representative', 'projects_involved', 'primary_provider', 'usage_summary',
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Customer', 'Topics', 'Representative', 'Projects', 'Provider', 'Usage Summary',
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('topics', 'usage_summary',)


class ProviderOverview(BaseSummaryView):
    """Overview of all providers of EUDAT services"""

    title = "EUDAT Provider"

    description = "All current and past providers of EUDAT CDI services"

    def content_items(self):
        """All providers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Provider')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'url', 'contact', 'contact_email', 
                'business_contact', 'business_email',
                'provider_type', 'provider_status', 'status_details',
                'infrastructure',
                'helpdesk_email',
                'security_contact',
                'created',
                'modified')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Provider', 'Website', 'Operational Contact', 'Email',
                'Business contact', 'Business email',
                'Type', 'Status', 'Status details',
                'Infrastructure Status',
                'Helpdesk email',
                'Security contact',
                'Created',
                'Modified')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('url', 'status_details', 'infrastructure', 'helpdesk_email', 
                'provider_status', 'provider_type')


class ServiceOverview(BaseSummaryView):
    """Overview of all EUDAT services"""

    title = "EUDAT Catalog"

    description = "All current and past EUDAT services"

    def content_items(self):
        """All services regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Service', path='/pcp/catalog')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'service_options', 'service_type', 'service_owner', 'contact',
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in hte specific classes"""
        return ('Title', 'Options', 'Type', 'Owner', 'Contact',
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('service_type',)


class ProjectOverview(BaseSummaryView):
    """Overview of all projects"""
    # almost identical to base class as this is the driving use case
    # implemented in the base class

    title = "Project Overview"

    description = "All current and past projects within the EUDAT CDI"

    def content_items(self):
        """All projects regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='Project')]


class RegisteredServiceOverview(BaseSummaryView):
    """Overview of all registered services no matter where they are"""

    title = "Registered Services"

    description = "All registered services of the EUDAT CDI"

    def content_items(self):
        """All registered services regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='RegisteredService')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'general_provider', 'contact', 'managers', 'monitored', 'scopes', 'service_components',
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Service name', 'General provider', 'Contact', 'Manager(s)', 'Monitored', 'Project scope(s)', 'Service component(s)',
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('monitored', 'scopes')


class RegisteredServiceComponentOverview(BaseSummaryView):
    """Overview of all registered services components no matter where they are located"""

    title = "Registered Service Components"

    description = "All registered service components of the EUDAT CDI"

    def content_items(self):
        """All registered service components regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='RegisteredServiceComponent')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'service_url', 'parent_provider', 'scopes', 'contacts',
                'monitored', 'host_name',
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Service component', 'URL', 'Provider', 'Project scope(s)', 'Contact(s)', 'Monitored', 'Host name',
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('service_url', 'monitored', 'host_name', 'scopes')


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
                'preferred_providers', 'created', 'modified', 'state')

    def field_labels(self):
        """Hardcoded label"""
        return ('Requesting Project', 'Request Type', 'Request Title', 'Requested Resources',
                'Requested Start Date', 'Preferred Provider(s)', 'Created', 'Modified', 'State')


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
        return ('title', 'parent_provider', 'provider_contact_email', 'provider_business_email',
                'compute_resources', 'storage_resources', 'scopes', 
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Resource name', 'Provider', 'Operational contact (email)', 'Business contact (email)',
                'Compute resources', 'Storage resources', 'Project scope(s)', 
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('compute_resources', 'storage_resources', 'scopes')

class RegisteredStorageResourceOverview(BaseSummaryView):
    """Overview of all registered storage resources no matter where they are located"""

    title = "Registered Storage Resources"

    description = "All registered storage resources across the entire site."

    def content_items(self):
        """All registered storage resources regardless of location"""
        return [element.getObject() for element in \
                self.catalog(portal_type='RegisteredStorageResource')]

    def fields(self):
        """Not yet complete - expand once we have accounting information"""
        return ('title', 'customer', 'project', 'parent_provider', 'scopes', 'services', \
                'storage_class', 'number', 
                'usage', 'allocated', 'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Storage Name', 'Customer', 'Project', 'Provider', 'Project scope(s)', 'Deployed on', \
                'Storage Class', 'Registered Objects', 
                'Used Storage', 'Allocated Storage', 'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('usage', 'allocated', 'storage_class', 'scopes')


class ServiceOfferOverview(BaseSummaryView):
    """Overview of all service offers no matter which provider makes them"""

    title = "Service Offers"

    description = "All service offers from all providers."

    def content_items(self):
        """All service offers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='ServiceOffer')]

    def fields(self):
        """Fields to show in the overview"""
        return ('title', 'service', 'parent_provider', 'slas', 'constraints', 'contact',
                'state', 'created', 'modified')

    def field_labels(self):
        """Explicit labels fo rthe fields"""
        return ('Service (offer)', 'Service (in catalog)', 'Provider', 'SLAs/OLAs', 'Constraints', 'Contact',
                'State', 'Created', 'Modified')


class ServiceComponentOfferOverview(BaseSummaryView):
    """Overview of all service component offers no matter which provider makes them"""

    title = "Service Component Offers"

    description = "All service component offers from all providers."

    def content_items(self):
        """All service component offers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='ServiceComponentOffer')]

    def fields(self):
        """Fields to show in the overview"""
        return ('title', 'service_component', 'implementations', 
                'parent_provider', 'slas', 'constraints',
                'state', 'created', 'modified')

    def field_labels(self):
        """Explicit labels fo rthe fields"""
        return ('Service Component (offer)', 'Service Component (in catalog)', 'Implementations supported', 
                'Provider', 'SLAs/OLAs', 'Constraints',
                'State', 'Created', 'Modified')


class ResourceOfferOverview(RegisteredResourceOverview):
    """Overview of all resource offers no matter which provider made them"""

    title = "Resource Offers"

    description = "All resource offers from all providers."

    def content_items(self):
        """All resource offers regardless of location"""
        return [element.getObject() for element in self.catalog(portal_type='ResourceOffer')]

    def fields(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('title', 'parent_provider', 'provider_contact_email', 'provider_business_email',
                'compute_resources', 'storage_resources', 'constraints', 
                'created', 'modified', 'state')

    def field_labels(self):
        """hardcoded for a start - to be overwritten in the specific classes"""
        return ('Resource offer', 'Provider', 'Operational contact (email)', 'Business contact (email)',
                'Compute resources', 'Storage resources', 'Constraints', 
                'Created', 'Modified', 'State')

    def simple_fields(self):
        """Manually maintained subset of fields where it is safe to just render the widget."""
        return ('compute_resources', 'storage_resources')

class DowntimeOverview(BaseSummaryView):

    title = "Downtimes"

    description = ""

    def content_items(self):
        return [element.getObject() for element in self.catalog(portal_type='Downtime')]

    def fields(self):
        return ('title', 'startDateTime', 'endDateTime', 
                'affected_registered_serivces', 
                'parent_provider', 'created', 'modified', 'state',)

    def field_labels(self):
        return ('Title', 'Start Date (UTC)', 'End Date (UTC)', 
                'Affected Services and Components', 
                'Provider', 'Created', 'Modified', 'State',)

    def simple_fields(self):
        return ('startDateTime', 'endDateTime', )


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
