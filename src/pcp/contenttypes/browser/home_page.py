from zope.interface import alsoProvides
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView


class HomePage(BrowserView):
    """Logic needed for the homepage view"""

    def __init__(self, context, request):
        """ Initialize context and request as view multi adaption parameters.
        """
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request

    def newbie(self):
        """True if 'Member' role not assigned"""
        roles = api.user.get_roles(obj=self.context)
        # print roles
        return 'Member' not in roles
