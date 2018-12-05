
import furl
import requests
from plone.protect.interfaces import IDisableCSRFProtection

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

from ..interfaces.settings import ISettings


class ProviderEngagement(BrowserView):

    def backlinks(self):
        return self.context.getBRefs('general_provider')

    def projects(self):
        return [p for p in self.backlinks() if p.portal_type == "Project"]

    def services(self):
        return [s for s in self.backlinks() if s.portal_type == "RegisteredService"]

    def components(self):
        return self.context.listFolderContents(contentFilter={"portal_type" : "RegisteredServiceComponent"})

    def storage(self):
        return self.context.listFolderContents(contentFilter={"portal_type" : "RegisteredStorageResource"})

    def project_data(self):
        result = []
        for p in self.projects():
            data = {}
            data['title'] = p.Title()
            data['url'] = p.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (p.absolute_url(), p.Title())
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
            data['title_with_link'] = '<a href="%s">%s</a>' % (s.absolute_url(), s.Title())
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
            data['title_with_link'] = '<a href="%s">%s</a>' % (c.absolute_url(), c.Title())
            data['created'] = c.created().Date()
            data['modified'] = c.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(c, 'review_state')
            result.append(data.copy())
        return result
        
    def storage_data(self):
        result = []
        for r in self.components():
            data = {}
            data['title'] = r.Title()
            data['url'] = r.absolute_url()
            data['title_with_link'] = '<a href="%s">%s</a>' % (r.absolute_url(), r.Title())
            data['created'] = r.created().Date()
            data['modified'] = r.modified().Date()
            data['state'] = self.context.portal_workflow.getInfoFor(r, 'review_state')
            result.append(data.copy())
        return result
        


