from plone.stringinterp import _
from plone.stringinterp.adapters import BaseSubstitution
from Products.CMFCore.interfaces import IContentish
from zope.component import adapts


class DPMTRequestSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _('Service or resource requests')
    description = _('Requested items')

    def safe_call(self):
        try:
            value = self.context.request_details()
        except AttributeError:
            value = _('No request specification found.')
        return value


class DPMTProviderSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _('Service or resource requests')
    description = _('Preferred providers')

    def safe_call(self):
        try:
            value = self.context.providers2string()
        except AttributeError:
            value = _('not specified')
        return value


class DPMTStartDateSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _('Service or resource requests')
    description = _('Start date')

    def safe_call(self):
        try:
            value = self.context.getStartDate()
            return value.Date()
        except AttributeError:
            return _('not specified')


class DPMTUsersToNotifySubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _('Service or resource requests')
    description = _('Users to notify')

    def safe_call(self):
        try:
            users = self.context.users_to_notify()
            return ','.join(users)
        except AttributeError:
            return _('not specified')
