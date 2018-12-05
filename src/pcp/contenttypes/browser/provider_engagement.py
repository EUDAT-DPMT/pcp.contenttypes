
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
        

