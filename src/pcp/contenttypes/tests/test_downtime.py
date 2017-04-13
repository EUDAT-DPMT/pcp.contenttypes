import re

import plone
import transaction
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from pcp.contenttypes.portlets.downtimes import Assignment
from pcp.contenttypes.testing import PCP_CONTENTTYPES_FUNCTIONAL_TESTING
from pcp.contenttypes.tests.base import FunctionalTestCase
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.container.interfaces import INameChooser


class TestDowntime(FunctionalTestCase):

    layer = PCP_CONTENTTYPES_FUNCTIONAL_TESTING

    TEST_OTHER_PROVIDER = 'aaaaaa111111'

    TEST_OTHER_DOWNTIME = 'Other Downtime'
    TEST_OTHER_DOWNTIME_START = DateTime('2017/04/13 12:44 UTC')
    TEST_OTHER_DOWNTIME_END = DateTime('2017/05/14 12:46 UTC')

    TEST_PAST_DOWNTIME = 'Past Downtime'
    TEST_PAST_DOWNTIME_START = DateTime('2016/04/13 12:44 UTC')
    TEST_PAST_DOWNTIME_END = DateTime('2016/05/14 12:46 UTC')

    TEST_PROVIDER_NAME = 'abcdef123456'
    TEST_PROVIDER_ID = 'abcdef123456_ID'
    TEST_PROVIDER_CITY = 'Schnedderedeng'
    TEST_PROVIDER_COUNTRY = 'Afghanistan'
    TEST_DOWNTIME_TITLE = 'Das ganze Scheisshaus steht in Flammen'
    TEST_DOWNTIME_DESCRIPTION = 'Sogar der Arsch ist in Gefahr'
    TEST_DOWNTIME_START = ('2017', 'July', '13', '05', '15')
    TEST_DOWNTIME_START_STRING = '2017/07/13 05:15:00 UTC'
    TEST_DOWNTIME_END = ('2017', 'July', '14', '18', '30')
    TEST_DOWNTIME_END_STRING = '2017/07/14 18:30:00 UTC'

    def fillInDateWidget(self, browser, field, date):
        browser.getControl(name=field+'-year').displayValue = [date[0]]
        browser.getControl(name=field+'-month').displayValue = [date[1]]
        browser.getControl(name=field+'-day').displayValue = [date[2]]
        browser.getControl(name=field+'-hour').displayValue = [date[3]]
        browser.getControl(name=field+'-minute').displayValue = [date[4]]

    def assertDateWidget(self, browser, field, date):
        self.assertEquals(browser.getControl(name=field+'-year').displayValue[0], date[0])
        self.assertEquals(browser.getControl(name=field+'-month').displayValue[0], date[1])
        self.assertEquals(browser.getControl(name=field+'-day').displayValue[0], date[2])
        self.assertEquals(browser.getControl(name=field+'-hour').displayValue[0], date[3])
        self.assertEquals(browser.getControl(name=field+'-minute').displayValue[0], date[4])

    def assertContainsDowntimeFull(self, browser):
        self.assertContainsDowntimeShort(browser)
        self.assertTrue(self.TEST_DOWNTIME_DESCRIPTION in browser.contents)

    def assertContainsDowntimeShort(self, browser):
        self.assertTrue(self.TEST_DOWNTIME_TITLE in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_START_STRING in browser.contents)
        self.assertTrue(self.TEST_DOWNTIME_END_STRING in browser.contents)

    def test(self):
        # Execute a browser test for downtime to ensure correct time formats and
        # timezone handling.

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

        self.portal.Providers.invokeFactory('Provider', self.TEST_OTHER_PROVIDER)
        otherProvider = self.portal.Providers[self.TEST_OTHER_PROVIDER]
        otherProvider.update(title=self.TEST_OTHER_PROVIDER)

        otherProvider.invokeFactory('Downtime', self.TEST_OTHER_DOWNTIME)
        otherDowntime = otherProvider[self.TEST_OTHER_DOWNTIME]
        otherDowntime.update(title=self.TEST_OTHER_DOWNTIME,
                             startDateTime=self.TEST_OTHER_DOWNTIME_START,
                             endDateTime=self.TEST_OTHER_DOWNTIME_END)

        otherProvider.invokeFactory('Downtime', self.TEST_PAST_DOWNTIME)
        pastDowntime = otherProvider[self.TEST_PAST_DOWNTIME]
        pastDowntime.update(title=self.TEST_PAST_DOWNTIME,
                            startDateTime=self.TEST_PAST_DOWNTIME_START,
                            endDateTime=self.TEST_PAST_DOWNTIME_END)

        otherDowntime.reindexObject()
        plone.api.content.transition(obj=otherDowntime, transition='publish')

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

        # Create provider
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

        # Create downtime
        browser.follow('Add new')
        self.assertTrue('Add new item' in browser.contents)
        browser.getControl(label='Downtime').click()
        browser.getControl(name='form.button.Add').click()

        self.assertTrue('Add Downtime' in browser.contents)
        browser.getControl(name='title').value = self.TEST_DOWNTIME_TITLE
        browser.getControl(name='description').value = self.TEST_DOWNTIME_DESCRIPTION
        self.fillInDateWidget(browser, 'startDateTime', self.TEST_DOWNTIME_START)
        self.fillInDateWidget(browser, 'endDateTime', self.TEST_DOWNTIME_END)
        browser.getControl(name='form.button.save').click()

        # Publish
        browser.follow('Publish')
        browser.getControl(name='form.button.confirm').click()

        # Check detail view
        self.assertContainsDowntimeFull(browser)

        # Check overview
        browser.open(portal_url + '/downtime_overview')
        self.assertContainsDowntimeShort(browser)

        # Back to detail view and edit
        browser.follow('Das ganze Schei')
        browser.follow('Edit')

        # Check edit view for correct dates
        self.assertDateWidget(browser, 'startDateTime', self.TEST_DOWNTIME_START)
        self.assertDateWidget(browser, 'endDateTime', self.TEST_DOWNTIME_END)

        # Check portlet on portal site
        browser.open(portal_url)
        open('/home/bernhard/crapp.html', 'w').write(browser.contents)
        self.assertTrue('All Downtimes...' in browser.contents)
        self.assertContainsDowntimeShort(browser)
        self.assertFalse(re.search('Upcoming Downtimes\\s+?\\(' + self.TEST_PROVIDER_NAME, browser.contents))
        self.assertTrue(self.TEST_OTHER_DOWNTIME in browser.contents)
        self.assertFalse(self.TEST_PAST_DOWNTIME in browser.contents)

        # Check portlet on provider overview site
        browser.follow('Providers')
        self.assertContainsDowntimeShort(browser)
        self.assertFalse(re.search('Upcoming Downtimes\\s+?\\(' + self.TEST_PROVIDER_NAME, browser.contents))
        self.assertTrue(self.TEST_OTHER_DOWNTIME in browser.contents)
        self.assertFalse(self.TEST_PAST_DOWNTIME in browser.contents)

        # Check portlet on provider detail site
        browser.follow(self.TEST_PROVIDER_NAME)
        open('/home/bernhard/crap.html', 'w').write(browser.contents)
        self.assertContainsDowntimeShort(browser)
        self.assertTrue(re.search('Upcoming Downtimes\\s+?\\(' + self.TEST_PROVIDER_NAME, browser.contents))
        self.assertFalse(self.TEST_OTHER_DOWNTIME in browser.contents)
        self.assertFalse(self.TEST_PAST_DOWNTIME in browser.contents)


