import glob
import json
import os

import plone
import transaction
from Products.ATBackRef import BackReferenceField
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes.Field import ReferenceField
from Products.CMFCore.utils import getToolByName
from mock import patch, call, MagicMock
from pcp.contenttypes.browser.accounting import Accounting
from pcp.contenttypes.testing import PCP_CONTENTTYPES_FUNCTIONAL_TESTING
from pcp.contenttypes.tests.base import FunctionalTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles


class TestFunctional(FunctionalTestCase):

    layer = PCP_CONTENTTYPES_FUNCTIONAL_TESTING

    def browseSite(self):
        transaction.commit()

        from plone.testing.z2 import Browser
        browser = Browser(self.app)
        browser.handleErrors = False

        portal_url = self.portal.absolute_url()
        self.portal.error_log._ignored_exceptions = ()

        browser.open(portal_url + '/login_form')
        browser.getControl(name='__ac_name').value = TEST_USER_NAME
        browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        browser.getControl(name='submit').click()

        self.assertIn('You are now logged in', browser.contents)
        return browser

    def afterSetUp(self):
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        test_directory = os.path.dirname(__file__)
        filenames = glob.glob(test_directory + '/testdata/*')

        file_contents = [open(filename).read() for filename in filenames]
        tables = [json.loads(content)[0] for content in file_contents]

        tables_by_id = {table['id']: table for table in tables}

        portal_types = getToolByName(self.portal, 'portal_types')
        # First pass of bootstrapping the content:
        # Create plain objects with attributes required for second pass only (UID).
        # This way we do not need to care about order of resolution of references.
        for obj_id, table in tables_by_id.items():
            portal_type = table['portal_type']
            # Create all objects in site root independently of scoping.
            portal_types.getTypeInfo(portal_type).global_allow = True
            self.portal.invokeFactory(portal_type, obj_id)
            obj = self.portal[obj_id]
            obj._setUID(table['uid'])

        # Second and final pass of bootstrapping:
        # Actually assign all properties in table. References can be set in any order as
        # the all objects already exist.
        for obj_id, table in tables_by_id.items():
            obj = self.portal[obj_id]

            # Treat table for application
            table.pop('id')

            for field in obj.Schema().fields():
                field_name = field.getName()
                # Set references only once (forward ones).
                # Check BackReferenceField before ReferenceField because
                # BackRefField derives from RefField.
                if isinstance(field, BackReferenceField):
                    table.pop(field_name)
                    continue
                # References are stored in a more detailed format than expected by fields.
                # Therefore strip down.
                elif isinstance(field, ReferenceField):
                    pure_uids = [reference['uid'] for reference in table[field_name]]
                    table[field_name] = pure_uids
                # Vocabulary not available in fixtureq
                # TODO: make named vocabulary available in fixture
                elif isinstance(field.vocabulary, NamedVocabulary):
                    table.pop(field_name)
                    continue

            obj.update(**table)

    @patch('pcp.contenttypes.content.downtime.send_mail')
    def test_downtimeNotification(self, send_mail):
        def assertMailsSent(subject, template):
            self.assertEquals(3, send_mail.call_count)
            self.assertEquals({'mfn-admin-1@example.com', 'mfn-admin-2@example.com', 'g.m.hagedorn@gmail.com'},
                              {args[1]['recipients'][0] for args in send_mail.call_args_list})
            for args in send_mail.call_args_list:
                self.assertEquals(1, len(args[1]['recipients']))
                self.assertIsNone(args[1]['sender'])
                self.assertEquals(subject, args[1]['subject'])
                self.assertEquals(template, args[1]['template'])

            send_mail.reset_mock()

        affectedRegisteredServiceComponent = self.portal['irods0--eudat.esc.rzg.mpg.de_24']
        provider = self.portal['MPCDF']
        provider.invokeFactory('Downtime', 'downtime')
        downtime = provider['downtime']
        downtime.update(title='Downtime Title',
                        description='Downtime Description',
                        startDateTime='2017-05-13 12:56 UTC',
                        endDateTime='2018-06-17 09:45 UTC',
                        affected_registered_serivces=(affectedRegisteredServiceComponent,))

        # Take a tour through the workflow graph and check for mails being sent
        # if and only if they shall be sent.

        self.assertEquals(plone.api.content.get_state(downtime), 'private')

        plone.api.content.transition(obj=downtime, transition='publish')
        assertMailsSent('[DPMT] Upcoming Downtime', 'announce-downtime.txt')

        self.assertEquals(plone.api.content.get_state(downtime), 'published')

        plone.api.content.transition(obj=downtime, transition='retract')
        assertMailsSent('[DPMT] Retracted Downtime', 'retract-downtime.txt')

        self.assertEquals(plone.api.content.get_state(downtime), 'private')

        plone.api.content.transition(obj=downtime, transition='submit')
        self.assertEquals(plone.api.content.get_state(downtime), 'pending')
        self.assertEquals(0, send_mail.call_count)

        plone.api.content.transition(obj=downtime, transition='reject')
        self.assertEquals(plone.api.content.get_state(downtime), 'private')
        self.assertEquals(0, send_mail.call_count)

        plone.api.content.transition(obj=downtime, transition='submit')
        self.assertEquals(plone.api.content.get_state(downtime), 'pending')
        self.assertEquals(0, send_mail.call_count)

        plone.api.content.transition(obj=downtime, transition='publish')
        assertMailsSent('[DPMT] Upcoming Downtime', 'announce-downtime.txt')

        self.assertEquals(plone.api.content.get_state(downtime), 'published')

        plone.api.content.transition(obj=downtime, transition='reject')
        assertMailsSent('[DPMT] Retracted Downtime', 'retract-downtime.txt')

        self.assertEquals(plone.api.content.get_state(downtime), 'private')

    # Keep order!
    ACCOUNTING_DATA = [
            {
                "core": {"value": "123", "unit": "B", "type": "storage"},
                "meta": {"submission_time": "2017-11-23 17:23:29", "ts": 17},
            },
            {
                "core": {"value": "124", "unit": "B", "type": "storage"},
                "meta": {"submission_time": "2017-11-23 16:23:29", "ts": 13},
            },
        ]

    @patch('pcp.contenttypes.browser.accounting.requests.get')
    def test_accountingCache(self, get):
        resource = self.portal['mfn-b2safe']

        result = MagicMock()
        result.ok = True
        result.json = MagicMock(return_value=self.ACCOUNTING_DATA)
        get.return_value = result

        response_text = Accounting(self.portal, self.request).update_record_caches()

        self.assertEquals(1, get.call_count)
        self.assertTrue(resource.UID() in get.call_args[0][0])
        self.assertTrue('/listRecords' in get.call_args[0][0])

        self.assertTrue(resource.title in response_text)

        self.assertEquals(resource.cached_records, self.ACCOUNTING_DATA)
        self.assertEquals(resource.cached_newest_record, self.ACCOUNTING_DATA[0])

    @patch('pcp.contenttypes.browser.accounting.requests.get')
    def test_accountingTab(self, get):
        resource = self.portal['mfn-b2safe']

        def get_impl(path):
            result = MagicMock()
            result.ok = True
            if 'listRecords' in path:
                result.json = MagicMock(return_value=self.ACCOUNTING_DATA)
            elif 'hasAccount' in path:
                result.json = MagicMock(return_value=dict(exists=True))
            return result

        get.side_effect = get_impl

        browser = self.browseSite()

        browser.open(resource.absolute_url())
        browser.follow('Accounting')

        self.assertTrue(get.call_count, 1)
        for record in self.ACCOUNTING_DATA:
            self.assertTrue(record['core']['value'] in browser.contents)
            self.assertTrue(record['meta']['submission_time'] in browser.contents)

    def test_accountingProjectView(self):
        self.fail('to be implemented')

    def test_rolerequest(self):
        self.fail('to be implemented')
