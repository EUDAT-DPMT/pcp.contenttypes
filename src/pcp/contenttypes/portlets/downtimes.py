from pcp.contenttypes.content_dx.provider import IProvider
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer

import datetime


class IDowntimePortlet(IPortletDataProvider):
    pass


@implementer(IDowntimePortlet)
class Assignment(base.Assignment):
    @property
    def title(self):
        return 'Upcoming Downtimes'


class AddForm(base.AddForm):
    # Parameters
    # *  count of downtimes to display
    # *  query time range
    schema = IDowntimePortlet
    label = u"Add Upcoming Downtime Portlet"
    description = u"Display upcoming Downtimes."

    def create(self, data):
        return Assignment()


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('downtimes.pt')

    def local_time(self, dt):
        return self.toLocalizedTime(dt, long_format=1)

    def getProvider(self):
        chain = self.context.aq_chain
        for element in chain:
            if IProvider.providedBy(element):
                return element
        return None

    def _getCurrentTimeInUtc(self):
        # Factor out this call from getDowntimes to enable patching utcnow.
        return datetime.datetime.utcnow()

    def getDowntimes(self):
        catalog = self.context.portal_catalog

        provider = self.getProvider()
        if provider:
            query = '/'.join(provider.getPhysicalPath())
        else:
            query = '/'

        query_path = {
            'query': query,
            'depth': 9,
        }

        now = self._getCurrentTimeInUtc()
        start = now + datetime.timedelta(-1)
        end = now + datetime.timedelta(365000)
        date_query = {'query': (start, end), 'range': 'min:max'}

        downtimeBrains = catalog(
            portal_type='downtime_dx',
            path=query_path,
            end=date_query,
            review_state='published',
            sort_on='start',
            sort_limit=10,
        )

        return [brain.getObject() for brain in downtimeBrains]
