"""Mixin class for content that is accountable (like resources)
"""
from pcp.contenttypes.interfaces.settings import ISettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import Interface

import furl
import json
import os
import requests



class IAccountable(Interface):
    """ Marker interface for content items that are accountable """


class Accountable(object):
    """Mixin class for things that are accountable"""

    def addAccount(self):
        """ Create IAccount folder on the accounting server """

        owner_id = self.getProvider().provider_userid
        if not owner_id:
            raise ValueError('Provider object has no provider_userid set')

        registry = getUtility(IRegistry)
        f_base = registry['dpmt.accounting_url']
        settings = registry.forInterface(ISettings, check=False)
        #f = furl.furl(settings.accounting_url + '/addAccount')
        f = furl.furl(f_base + '/addAccount')
        credentials = (registry['dpmt.accounting_username'],
                       registry['dpmt.accounting_password'])
        data = dict(id=self.UID(), owner=owner_id)
        result = requests.post(f, data=data, auth=credentials)
        if not result.ok:
            raise RuntimeError('Unable to create account for {} on accounting server (reason: {})'.format(
                owner_id, result.text))

    def getProvider(self):
        """The provider offering the accountable resource. """
        # assume the acquisition parent to be the provider
        return self.aq_inner.aq_parent
