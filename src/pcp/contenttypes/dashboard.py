# -*- coding: utf-8 -*-
from pcp.contenttypes.portlets import downtimes
from plone.app.portlets import portlets
from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.portlets.interfaces import IDefaultDashboard
from zope.interface import implementer


@implementer(IDefaultDashboard)
class PCPDefaultDashboard(DefaultDashboard):
    """A override of the default dashboard.
    """

    def __call__(self):
        return {
            'plone.dashboard1': (portlets.news.Assignment(), ),
            'plone.dashboard2': (portlets.recent.Assignment(), ),
            'plone.dashboard3': (downtimes.Assignment(), ),
            'plone.dashboard4': (portlets.review.Assignment(), ),
        }
