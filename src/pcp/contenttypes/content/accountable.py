"""Mixin class for content that is accountable (like resources)
"""

import os
import furl
import json
import requests

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from ..interfaces.settings import ISettings

class Accountable(object):
    """Mixin class for things that are accountable"""

    def addAccount(self):
        """ Create IAccount folder on the accounting server """

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        f = furl.furl(settings.accounting_url + '/addAccount')

        owner_id = self.getProvider().provider_userid
        if not owner_id:
            raise ValueError('Provider object has no provider_userid set')

        data = dict(
            id=self.UID(),
            owner=owner_id)
        result = requests.post(f, data=data)
        if not result.ok:
            raise RuntimeError('Unable to create account for {} on accounting server (reason: {})'.format(owner_id, result.text))
