import glob
import json
import os
import unittest

import plone
import transaction
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from mock import patch, call, MagicMock
from pcp.contenttypes.browser.accounting import Accounting
from pcp.contenttypes.testing import PCP_CONTENTTYPES_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from zope.component import getMultiAdapter
from zopyx.plone.persistentlogger.logger import IPersistentLogger


class TestFunctional(unittest.TestCase):

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
        browser.getControl(name='button.login').click()

        self.assertIn('You are now logged in', browser.contents)
        return browser

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        test_directory = os.path.dirname(__file__)
        filenames = glob.glob(test_directory + '/testdata/*')

        file_contents = [open(filename).read() for filename in filenames]
        tables = [json.loads(content)[0] for content in file_contents]

        tables_by_id = {table['id']: table for table in tables}

        # Switch to separate folder to avoid object names and urls occurring in
        # navigation to enable simple checking for them.
        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal.folder

        portal_types = getToolByName(self.portal, 'portal_types')
        # First pass of bootstrapping the content:
        # Create plain objects with attributes required for second pass only (UID).
        # This way we do not need to care about order of resolution of references.
        for obj_id, table in tables_by_id.items():
            portal_type = table['portal_type']
            # Create all objects in site root independently of scoping.
            portal_types.getTypeInfo(portal_type).global_allow = True
            self.folder.invokeFactory(portal_type, obj_id)
            obj = self.folder[obj_id]
            setattr(obj, '_plone.uuid', table['uid'])
            obj.reindexObject(idxs=['UID'])

        # Second and final pass of bootstrapping:
        # Actually assign all properties in table. References can be set in any order as
        # the all objects already exist.
        for obj_id, table in tables_by_id.items():
            obj = self.folder[obj_id]

            # Treat table for application
            table.pop('id')

            for field in obj.Schema().fields():
                field_name = field.getName()
                # Set references only once (forward ones).
                # Check BackReferenceField before ReferenceField because
                # BackRefField derives from RefField.
                # if isinstance(field, BackReferenceField):
                #     table.pop(field_name)
                #     continue
                # References are stored in a more detailed format than expected by fields.
                # Therefore strip down.
                # elif isinstance(field, ReferenceField):
                #     pure_uids = [reference['uid'] for reference in table[field_name]]
                #     table[field_name] = pure_uids
                # Vocabulary not available in fixtureq
                # TODO: make named vocabulary available in fixture
                # elif isinstance(field.vocabulary, NamedVocabulary):
                #     table.pop(field_name)
                #     continue

            obj.update(**table)

    @patch('pcp.contenttypes.content.downtime._getCurrentTime')
    @patch('pcp.contenttypes.content.downtime.send_mail')
    def test_downtimeNotification(self, send_mail, _getCurrentTime):
        _getCurrentTime.return_value = DateTime('2017-04-18 13:34 UTC')

        def assertMailsSent(subject, template):
            self.assertEquals(3, send_mail.call_count)
            self.assertEquals(
                {
                    'mfn-admin-1@example.com',
                    'mfn-admin-2@example.com',
                    'g.m.hagedorn@gmail.com',
                },
                {args[1]['recipients'][0] for args in send_mail.call_args_list},
            )
            for args in send_mail.call_args_list:
                self.assertEquals(1, len(args[1]['recipients']))
                self.assertIsNone(args[1]['sender'])
                self.assertEquals(subject, args[1]['subject'])
                self.assertEquals(template, args[1]['template'])

            send_mail.reset_mock()

        affectedRegisteredServiceComponent = self.folder[
            'irods0--eudat.esc.rzg.mpg.de_24'
        ]
        provider = self.folder['MPCDF']
        provider.invokeFactory('Downtime', 'downtime')
        downtime = provider['downtime']
        downtime.update(
            title='Downtime Title',
            description='Downtime Description',
            startDateTime='2017-05-13 12:56 UTC',
            endDateTime='2018-06-17 09:45 UTC',
            affected_registered_serivces=(affectedRegisteredServiceComponent,),
        )

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

        # also test filtering of notifications for past downtimes
        _getCurrentTime.return_value = DateTime('2020-03-04 18:34 UTC')

        plone.api.content.transition(obj=downtime, transition='publish')

        self.assertEquals(plone.api.content.get_state(downtime), 'published')
        self.assertEquals(0, send_mail.call_count)

        plone.api.content.transition(obj=downtime, transition='retract')

        self.assertEquals(plone.api.content.get_state(downtime), 'private')
        self.assertEquals(0, send_mail.call_count)

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
        resource = self.folder['mfn-b2safe']

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
    def test_accountingTabLiveData(self, get):
        resource = self.folder['mfn-b2safe']

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

    @patch('pcp.contenttypes.browser.accounting.requests.get')
    def test_accountingTabCachedData(self, get):
        resource = self.folder['mfn-b2safe']

        get.return_value = MagicMock(ok=False)

        browser = self.browseSite()

        browser.open(resource.absolute_url())
        with self.assertRaises(RuntimeError):
            browser.follow('Accounting')

        result = MagicMock()
        result.ok = True
        result.json = MagicMock(return_value=self.ACCOUNTING_DATA)
        get.return_value = result
        Accounting(self.portal, self.request).update_record_caches()

        get.return_value = MagicMock(ok=False)

        browser = self.browseSite()
        browser.open(resource.absolute_url())
        browser.follow('Accounting')

        self.assertTrue(get.call_count, 1)
        for record in self.ACCOUNTING_DATA:
            self.assertTrue(record['core']['value'] in browser.contents)
            self.assertTrue(record['meta']['submission_time'] in browser.contents)

    @patch('pcp.contenttypes.browser.accounting.requests.get')
    def test_accountingProjectView(self, get):
        project = self.folder['B2SAFEforMfN']

        browser = self.browseSite()
        browser.open(project.absolute_url())
        self.assertTrue('??' in browser.contents)

        result = MagicMock()
        result.ok = True
        result.json = MagicMock(return_value=self.ACCOUNTING_DATA)
        get.return_value = result
        Accounting(self.portal, self.request).update_record_caches()

        browser = self.browseSite()
        browser.open(project.absolute_url())

        record = self.ACCOUNTING_DATA[0]
        self.assertTrue(record['core']['value'] in browser.contents)
        self.assertTrue(record['meta']['submission_time'] in browser.contents)

    @patch('pcp.contenttypes.content.rolerequest.send_mail')
    def test_rolerequest(self, send_mail):
        def assertMailsSent(subject):
            self.assertEquals(1, send_mail.call_count)
            self.assertEquals(
                {'mfn-admin-1@example.com', 'mfn-admin-2@example.com'},
                send_mail.call_args[1]['recipients'],
            )
            for args in send_mail.call_args_list:
                self.assertEquals(2, len(args[1]['recipients']))
                self.assertIsNone(args[1]['sender'])
                self.assertEquals(subject, args[1]['subject'])
                self.assertEquals('role-request.txt', args[1]['template'])

            send_mail.reset_mock()

        username_requester = 'mfn-admin-2'
        username_receiver = 'mfn-admin-1'
        email_requester = 'mfn-admin-2@example.com'
        email_receiver = 'mfn-admin-1@example.com'
        location = self.folder['B2SAFE']
        role = 'Enabler'

        # Create users
        plone.api.user.create(email_receiver, username_receiver)
        plone.api.user.create(email_requester, username_requester, roles=('Manager',))

        # Use requester to create rolerequest
        logout()
        login(self.portal, username_requester)

        self.portal.invokeFactory('RoleRequest', 'rolerequest')
        rolerequest = self.portal.rolerequest

        rolerequest.update(
            Title='Role Request for Peter Lustig',
            userid=username_receiver,
            role=role,
            context=location,
            motivation='Motivation',
        )

        # Switch back to TEST_USER
        logout()
        login(self.portal, TEST_USER_NAME)

        # Take a tour through the transition graph checking mails being sent, permissions set and logged

        logger = IPersistentLogger(location)

        self.assertEquals('submitted', plone.api.content.get_state(rolerequest))
        self.assertEquals(0, send_mail.call_count)
        self.assertFalse(
            role
            in plone.api.user.get_roles(
                username=username_receiver, obj=location, inherit=False
            )
        )
        self.assertEquals(0, len(logger.entries))

        plone.api.content.transition(obj=rolerequest, transition='reject')

        self.assertEquals('rejected', plone.api.content.get_state(rolerequest))
        assertMailsSent('[DPMT] Role request rejected')
        self.assertFalse(
            role
            in plone.api.user.get_roles(
                username=username_receiver, obj=location, inherit=False
            )
        )
        self.assertEquals(0, len(logger.entries))

        plone.api.content.transition(obj=rolerequest, transition='submit')

        self.assertEquals('submitted', plone.api.content.get_state(rolerequest))
        self.assertEquals(0, send_mail.call_count)
        self.assertFalse(
            role
            in plone.api.user.get_roles(
                username=username_receiver, obj=location, inherit=False
            )
        )
        self.assertEquals(0, len(logger.entries))

        plone.api.content.transition(obj=rolerequest, transition='accept')

        self.assertEquals('accepted', plone.api.content.get_state(rolerequest))
        assertMailsSent('[DPMT] Role request accepted')
        self.assertTrue(
            role
            in plone.api.user.get_roles(
                username=username_receiver, obj=location, inherit=False
            )
        )
        self.assertEquals(1, len(logger.entries))

    def test_SummaryView_noCrashes(self):
        # This test checks that the fields referenced by the summaries actually exist and
        # that their rendering does not crash.
        # This test does not check if the output is correct.

        getToolByName(self.portal, 'portal_workflow').setDefaultChain(
            'intranet_workflow'
        )

        view_types = (
            (self.folder, 'customer_overview', 'Community'),
            (self.folder, 'provider_overview', 'Provider'),
            (self.folder, 'service_overview', 'Service'),
            (self.portal, 'project_overview', 'Project'),
            (self.portal, 'registered_service_overview', 'RegisteredService'),
            (
                self.portal,
                'registered_service_component_overview',
                'RegisteredServiceComponent',
            ),
            (self.portal, 'request_overview', 'ServiceRequest'),
            (self.portal, 'approved_requests', 'ServiceRequest'),
            (
                self.portal,
                'registered_storage_resource_overview',
                'RegisteredStorageResource',
            ),
            (self.portal, 'resource_offer_overview', 'ResourceOffer'),
            (self.portal, 'downtime_overview', 'Downtime'),
        )

        portal_types = getToolByName(self.portal, 'portal_types')
        index = 0
        for context, view_name, obj_type in view_types:
            portal_types.getTypeInfo(obj_type).global_allow = True
            obj_id = 'overview_test_object_%s_%s' % (obj_type, index)

            self.portal.invokeFactory(obj_type, obj_id)
            test_object = self.portal[obj_id]
            test_object.update(title=obj_id)

            view = getMultiAdapter((context, self.portal.REQUEST), name=view_name)
            try:
                text = view()
            except KeyError as e:
                # Here we get mismatches between overview's fields and schema
                self.fail(
                    'Rendering %s failed: maybe a typo of the field name: %s'
                    % (obj_type, e)
                )
            except Exception as e:
                # We get here most probably if something went wrong
                # when using a wrong renderer (i.e. if original is not available) for a field.
                self.fail(
                    'Rendering %s failed: maybe a missing renderer: %s' % (obj_type, e)
                )

            self.assertTrue(obj_id in text)

            # Explicitly check for a suitable renderer for each field because
            # there could exist a field type with values compatible with the reference renderer.
            for field in test_object.Schema().fields():
                name = field.getName()
                from Products.Archetypes.interfaces import IReferenceField

                self.assertTrue(
                    name not in view.fields()
                    or name in view.simple_fields()
                    or name in view.render_methods
                    or IReferenceField.providedBy(field)
                )

            index += 1

    def test_SummaryView_correctness(self):
        # This test creates objects such that each renderer is invoked once
        # and we can check the output for the expected text.
        # ServiceRequest uses all renderers except modification_date.

        portal_types = getToolByName(self.portal, 'portal_types')
        portal_types.getTypeInfo('ResourceRequest').global_allow = True

        # avoid the links being also part of navbar
        self.folder.invokeFactory('Folder', 'theFolder')
        theFolder = self.folder['theFolder']
        theFolder.setTitle('ResourceRequestFolder')

        theFolder.invokeFactory('ResourceRequest', 'resourceRequest')
        resourceRequest = theFolder.resourceRequest

        TEST_REQUEST_PARENT_PROJECT = (self.folder['B2SAFEforMfN'],)
        TEST_REQUEST_PREFERRED_PROVIDERS = (self.folder['MPCDF'],)
        TEST_REQUEST_TITLE = 'test-request-title'
        TEST_REQUEST_START_DATE = '2013/11/29'
        TEST_REQUEST_STORAGE_RESOURCES = (
            {'value': '17888', 'unit': 'EiB', 'storage class': 'nearline+'},
        )
        TEST_REQUEST_COMPUTE_RESOURCES = (
            {
                'nCores': '134861',
                'ram': '456634',
                'diskspace': '7456314',
                'system': 'Windows 3.1',
            },
        )

        resourceRequest.update(
            parent_project=TEST_REQUEST_PARENT_PROJECT,
            title=TEST_REQUEST_TITLE,
            startDate=TEST_REQUEST_START_DATE,
            preferred_providers=TEST_REQUEST_PREFERRED_PROVIDERS,
            storage_resources=TEST_REQUEST_STORAGE_RESOURCES,
            compute_resources=TEST_REQUEST_COMPUTE_RESOURCES,
        )

        # get a unique string to check for
        plone.api.content.transition(obj=resourceRequest, transition='submit')

        # get view and run it
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name='request_overview'
        )
        text = view()

        def assertNumOccurences(expectedCount, pattern):
            import re

            actualCount = len(re.findall(pattern, text))
            self.assertEquals(actualCount, expectedCount)

        # render_state
        assertNumOccurences(1, 'submitted')
        # render_type
        assertNumOccurences(1, 'Resource Request')
        # render_reference_field
        assertNumOccurences(1, TEST_REQUEST_PREFERRED_PROVIDERS[0].absolute_url())
        assertNumOccurences(
            2, TEST_REQUEST_PREFERRED_PROVIDERS[0].title
        )  # also in provider.absolute_url()
        # render_with_link
        assertNumOccurences(1, TEST_REQUEST_TITLE)
        assertNumOccurences(1, resourceRequest.absolute_url())
        # render_parent
        assertNumOccurences(
            2, theFolder.absolute_url()
        )  # also in serviceRequest.absolute_url()
        assertNumOccurences(1, 'ResourceRequestFolder')
        # render_date
        assertNumOccurences(1, TEST_REQUEST_START_DATE)
        # render_resources
        for key in ('Cores', 'RAM', 'disk'):
            assertNumOccurences(1, key)
        for key, value in TEST_REQUEST_COMPUTE_RESOURCES[0].items():
            assertNumOccurences(1, value)
        for key, value in TEST_REQUEST_STORAGE_RESOURCES[0].items():
            assertNumOccurences(1, value)
