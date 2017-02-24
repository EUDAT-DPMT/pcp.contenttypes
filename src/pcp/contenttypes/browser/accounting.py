
import furl
import requests

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView

from ..interfaces.settings import ISettings


class Accounting(BrowserView):

    def has_account(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        f = furl.furl(settings.accounting_url)
        if settings.accounting_username:
            f.username = settings.accounting_username
        if settings.accounting_password:
            f.password = settings.accounting_password
        f.path = str(f.path) + '/hasAccount'
        f.args['id'] = self.context.UID()
        url = str(f)
        result = requests.get(url)
        if result.ok:
            return result.json()['exists']
        else:
            raise RuntimeError('Unable to determine hasAccount status')

    def create_account(self):

        self.context.addAccount()
        self.request.response.redirect(self.context.absolute_url() + '/list-account-records')


    def records(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        f = furl.furl(settings.accounting_url)
        if settings.accounting_username:
            f.username = settings.accounting_username
        if settings.accounting_password:
            f.password = settings.accounting_password
        f.path = str(f.path) + '/' + self.context.UID() + '/listRecords'
        url = str(f)
        result = requests.get(url)
        if result.ok:
            results = result.json()
            for r in results:
                # XXX TODO figure out target unit from value 
                r['core'] = self.context.convert(r['core'], 'TiB')
            return results
        return ()

