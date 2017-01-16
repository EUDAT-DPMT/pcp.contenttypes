
import furl
import requests

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView

from ..interfaces.settings import ISettings


class Accounting(BrowserView):

    def records(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        f = furl.furl(settings.accounting_url)
        f.path = str(f.path) + '/' + self.context.UID() + '/listRecords'
        url = str(f)
        result = requests.get(url)
        if result.ok:
            return result.json()
        return ()
