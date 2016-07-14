from zope.component import adapts
from Products.CMFCore.interfaces import IContentish

from plone.stringinterp import _
from plone.stringinterp.adapters import BaseSubstitution


class DPMTRequestSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'Service or resource requests')
    description = _(u'Requested items')

    def safe_call(self):
        try:
            value = self.context.request_details()
        except AttributeError:
            value = _(u'No request specification found.')
        return value

class DPMTProviderSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'Service or resource requests')
    description = _(u'Preferred providers')

    def safe_call(self):
        try:
            value = self.context.providers2string()
        except AttributeError:
            value = _(u'not specified')
        return value
