import furl
import requests
from plone.protect.interfaces import IDisableCSRFProtection

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

from ..interfaces.settings import ISettings

# helper method for rendering reference fields
def render_reference_field(content, field_id, with_state=False):
    field = content.schema[field_id]
    objs = field.get(content, aslist=True)
    text = []
    if objs == []:
        return "no reference set"
    for item in objs:
        if with_state:
            state = content.portal_workflow.getInfoFor(item, 'review_state')
            text.append(
                "<a href='%s'>%s</a> (%s)" % (item.absolute_url(), item.Title(), state)
            )

        else:
            text.append("<a href='%s'>%s</a>" % (item.absolute_url(), item.Title()))
    return "<br />".join(text)


class ProviderEngagement(BrowserView):
    def backlinks(self):
        return self.context.getBRefs('general_provider')

    def projects(self):
        return [p for p in self.backlinks() if p.portal_type == "Project"]

    def services(self):
        return [s for s in self.backlinks() if s.portal_type == "RegisteredService"]

    def components(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "RegisteredServiceComponent"}
        )

    def storage(self):
        return self.context.listFolderContents(
            contentFilter={"portal_type": "RegisteredStorageResource"}
        )

    def project_data(self):
        result = []
        for p in self.projects():
            data = {}
            data['title'] = p.Title()
            data['url'] = p.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (
                p.absolute_url(),
                p.Title(),
            )
            customer = p.getCommunity()
            if customer not in [None, '']:
                data['customer_with_link'] = '<a href="%s">%s</a>' % (
                    customer.absolute_url(),
                    customer.Title(),
                )
            data['topics'] = p.getTopics()
            data['usage'] = p.getUsed_new()
            data['number'] = p.getRegistered_objects()
            data['created'] = p.created().Date()
            data['modified'] = p.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(p, 'review_state')
            result.append(data.copy())
        return result

    # Starting with code duplication so we can individually adapt later
    def service_data(self):
        result = []
        for s in self.services():
            data = {}
            data['title'] = s.Title()
            data['url'] = s.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (
                s.absolute_url(),
                s.Title(),
            )
            contact = s.getContact()
            data['contact'] = render_reference_field(s, 'contact')
            data['managers'] = render_reference_field(s, 'managers')
            data['components'] = render_reference_field(
                s, 'service_components', with_state=True
            )
            data['created'] = s.created().Date()
            data['modified'] = s.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(s, 'review_state')
            result.append(data.copy())
        return result

    def component_data(self):
        result = []
        for c in self.components():
            data = {}
            data['title'] = c.Title()
            data['url'] = c.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (
                c.absolute_url(),
                c.Title(),
            )
            data['service_url'] = '<a href="%s">%s</a>' % (
                c.getService_url(),
                c.getService_url(),
            )
            data['contacts'] = render_reference_field(c, 'contacts')
            data['created'] = c.created().Date()
            data['modified'] = c.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(c, 'review_state')
            result.append(data.copy())
        return result

    def storage_data(self):
        result = []
        for r in self.storage():
            data = {}
            data['title'] = r.Title()
            data['url'] = r.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (
                r.absolute_url(),
                r.Title(),
            )
            data['usage'] = r.getResourceUsage()
            data['number'] = r.getNumberOfRegisteredObjects(as_int=True)
            data['allocated'] = r.getAllocated()
            data['storage_class'] = r.getStorageClass()
            data['created'] = r.created().Date()
            data['modified'] = r.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(r, 'review_state')
            result.append(data.copy())
        return result
