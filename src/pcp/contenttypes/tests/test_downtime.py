import transaction
from Products.CMFCore.utils import getToolByName
from pcp.contenttypes.portlets.downtimes import Assignment
from pcp.contenttypes.testing import PCP_CONTENTTYPES_FUNCTIONAL_TESTING
from pcp.contenttypes.tests.base import FunctionalTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.portlets.constants import GROUP_CATEGORY
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.container.interfaces import INameChooser


class TestDowntime(FunctionalTestCase):

    layer = PCP_CONTENTTYPES_FUNCTIONAL_TESTING

    TEST_PROVIDER_NAME = 'abcdef123456'
    TEST_PROVIDER_ID = 'abcdef123456_ID'
    TEST_PROVIDER_CITY = 'Schnedderedeng'
    TEST_PROVIDER_COUNTRY = 'Afghanistan'
    TEST_DOWNTIME_TITLE = 'Das ganze Scheisshaus steht in Flammen'
    TEST_DOWNTIME_DESCRIPTION = 'Sogar der Arsch ist in Gefahr'
    TEST_DOWNTIME_START = ('2017', 'July', '13', '05', '15', 'AM')
    TEST_DOWNTIME_START_STRING = '2017-07-13 05:15 UTC'
    TEST_DOWNTIME_END = ('2017', 'July', '14', '06', '30', 'PM')
    TEST_DOWNTIME_END_STRING = '2017-07-14 18:30 UTC'

    def test(self):
        # Create a provider and within the provider a downtime for it.
        # Then check all occurrences of the downtime for correct values:
        # * downtime default view
        # * portlet
        # * overview

        setRoles(self.portal, TEST_USER_ID, ['Manager',])
        self.portal.invokeFactory('Folder', 'Providers')
        self.portal.Providers.invokeFactory('Provider', 'provider')
        self.portal.Providers.provider.invokeFactory('Downtime', 'downtime')
        getToolByName(self.portal, 'portal_workflow').setDefaultChain('intranet_workflow')
        column = getUtility(IPortletManager, 'plone.leftcolumn')
        manager = getMultiAdapter((self.portal, column), IPortletAssignmentMapping)
        assignment = Assignment()
        chooser = INameChooser(manager)
        manager[chooser.chooseName(None, assignment)] = assignment
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
        browser.open(portal_url)

        browser.follow('Providers')
        browser.follow('Add new')

        self.assertTrue('Add new item' in browser.contents)
        self.assertTrue('Compute or data service provider' in browser.contents)

        browser.getControl("Provider").click()
        browser.getControl(name='form.button.Add').click()

        browser.getControl(name="title").value = self.TEST_PROVIDER_NAME
        browser.getControl(name='provider_userid').value = self.TEST_PROVIDER_ID
        browser.getControl(name='address.city:record:ignore_empty').value = self.TEST_PROVIDER_CITY
        browser.getControl(name='address.country:record:ignore_empty').displayValue = [self.TEST_PROVIDER_COUNTRY]
        browser.getControl(name="form.button.save").click()

        browser.follow('Add new')
        self.assertTrue('Add new item' in browser.contents)
        browser.getControl(label='Downtime').click()
        browser.getControl(name='form.button.Add').click()

        self.assertTrue('Add Downtime' in browser.contents)
        browser.getControl(name='title').value = self.TEST_DOWNTIME_TITLE
        browser.getControl(name='description').value = self.TEST_DOWNTIME_DESCRIPTION
        browser.getControl(name='startDateTime_year').displayValue = [self.TEST_DOWNTIME_START[0]]
        browser.getControl(name='startDateTime_month').displayValue = [self.TEST_DOWNTIME_START[1]]
        browser.getControl(name='startDateTime_day').displayValue = [self.TEST_DOWNTIME_START[2]]
        browser.getControl(name='startDateTime_hour').displayValue = [self.TEST_DOWNTIME_START[3]]
        browser.getControl(name='startDateTime_minute').displayValue = [self.TEST_DOWNTIME_START[4]]
        browser.getControl(name='startDateTime_ampm').displayValue = [self.TEST_DOWNTIME_START[5]]
        browser.getControl(name='endDateTime_year').displayValue = [self.TEST_DOWNTIME_END[0]]
        browser.getControl(name='endDateTime_month').displayValue = [self.TEST_DOWNTIME_END[1]]
        browser.getControl(name='endDateTime_day').displayValue = [self.TEST_DOWNTIME_END[2]]
        browser.getControl(name='endDateTime_hour').displayValue = [self.TEST_DOWNTIME_END[3]]
        browser.getControl(name='endDateTime_minute').displayValue = [self.TEST_DOWNTIME_END[4]]
        browser.getControl(name='endDateTime_ampm').displayValue = [self.TEST_DOWNTIME_END[5]]
        browser.getControl(name='form.button.save').click()

        open('/home/bernhard/crap.html', 'w').write(browser.contents)

        self.assertTrue(self.TEST_DOWNTIME_TITLE in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_END_STRING in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_START_STRING in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_DESCRIPTION in browser.contents)

        browser.open(portal_url + '/downtime_overview')

        self.assertTrue(self.TEST_DOWNTIME_TITLE in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_END_STRING in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_START_STRING in browser.contents)

        browser.follow('Das ganze Schei')
        browser.follow('Edit')

        self.assertEquals(browser.getControl(name='startDateTime_year').displayValue[0], self.TEST_DOWNTIME_START[0])
        self.assertEquals(browser.getControl(name='startDateTime_month').displayValue[0], self.TEST_DOWNTIME_START[1])
        self.assertEquals(browser.getControl(name='startDateTime_day').displayValue[0], self.TEST_DOWNTIME_START[2])
        self.assertEquals(browser.getControl(name='startDateTime_hour').displayValue[0], self.TEST_DOWNTIME_START[3])
        self.assertEquals(browser.getControl(name='startDateTime_minute').displayValue[0], self.TEST_DOWNTIME_START[4])
        self.assertEquals(browser.getControl(name='startDateTime_ampm').displayValue[0], self.TEST_DOWNTIME_START[5])

