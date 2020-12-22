from ..interfaces.settings import ISettings
from plone.protect.interfaces import IDisableCSRFProtection
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getUtility
from zope.interface import alsoProvides

import furl
import requests


class Accounting(BrowserView):
    def has_account(self):
        registry = getUtility(IRegistry)
        # settings = registry.forInterface(ISettings, check=False)
        # f = furl.furl(settings.accounting_url)
        # if settings.accounting_username:
        #    f.username = settings.accounting_username
        # if settings.accounting_password:
        #    f.password = settings.accounting_password
        f = furl.furl(registry['dpmt.accounting_url'])
        f.username = registry['dpmt.accounting_username']
        f.password = registry['dpmt.accounting_password']
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
            self.context.absolute_url() + '/list-account-records'
        )

    def records(self):
        resource = self.context
        records = self.fetch_records(resource.UID())
        if records:
            return records
        else:
            return getattr(resource, 'cached_records', ())

    def fetch_records(self, uid):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISettings, check=False)
        f = furl.furl(registry['dpmt.accounting_url'])
        f.username = registry['dpmt.accounting_username']
        f.password = registry['dpmt.accounting_password']
        # if settings.accounting_username:
        #    f.username = settings.accounting_username
        # if settings.accounting_password:
        #    f.password = settings.accounting_password
        f.path = str(f.path) + '/' + uid + '/listRecords'
        url = str(f)
        result = requests.get(url)
        if result.ok:
            results = result.json()
            return results
        return ()

    def update_record_caches(self):
        alsoProvides(self.request, IDisableCSRFProtection)

        catalog = self.context.portal_catalog
        resource_brains = catalog(
            portal_type=['RegisteredStorageResource', 'registeredstorageresource_dx']
        )
        updated_resources = []

        for brain in resource_brains:
            resource = brain.getObject()
            records = self.fetch_records(resource.UID())
            if records:
                newest_record = max(records, key=lambda x: x['meta']['submission_time'])
                resource.cached_records = records
                resource.cached_newest_record = newest_record
            updated_resources.append(resource.title)

        return 'Updated resource record caches:\n\n' + '\n'.join(updated_resources)
