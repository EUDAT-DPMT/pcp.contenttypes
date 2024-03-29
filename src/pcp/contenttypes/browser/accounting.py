
import furl
import requests
from plone.protect.interfaces import IDisableCSRFProtection

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides

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
            if hasattr(self.context, 'cached_records'):
                return True
            else:
                raise RuntimeError('Unable to determine hasAccount status')

    def create_account(self):

        self.context.addAccount()
        self.request.response.redirect(
            self.context.absolute_url() + '/list-account-records')

    def records(self, n=10):
        n = self.request.get('n', n)
        resource = self.context
        records = self.fetch_records(resource.UID(), n)
        if records:
            return records
        else:
            return getattr(resource, 'cached_records', ())


    def fetch_records(self, uid, n=11):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings)
        f = furl.furl(settings.accounting_url)
        if settings.accounting_username:
            f.username = settings.accounting_username
        if settings.accounting_password:
            f.password = settings.accounting_password
        f.path = str(f.path) + '/' + uid + '/listRecords'
        f.args['n'] = n
        url = str(f)
        result = requests.get(url)
        if result.ok:
            results = result.json()
            return results
        return ()


    def update_record_caches(self):
        alsoProvides(self.request, IDisableCSRFProtection)

        catalog = self.context.portal_catalog
        resource_brains = catalog(portal_type='RegisteredStorageResource')
        updated_resources = []

        for brain in resource_brains:
            resource = brain.getObject()
            records = self.fetch_records(resource.UID())
            if records:
                newest_record = max(records, key=lambda x: x['meta']['submission_time'])
                resource.cached_records = records
                resource.cached_newest_record = newest_record
            updated_resources.append(resource.title)

        return "Updated resource record caches:\n\n" + '\n'.join(updated_resources)
