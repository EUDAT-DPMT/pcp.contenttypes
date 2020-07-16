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


class DPMTStartDateSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'Service or resource requests')
    description = _(u'Start date')

    def safe_call(self):
        try:
            value = self.context.getStartDate()
            return value.Date()
        except AttributeError:
            return _(u'not specified')


class DPMTUsersToNotifySubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'Service or resource requests')
    description = _(u'Users to notify')

    def safe_call(self):
        try:
            users = self.context.users_to_notify()
            return u','.join(users)
        except AttributeError:
            return _(u'not specified')
