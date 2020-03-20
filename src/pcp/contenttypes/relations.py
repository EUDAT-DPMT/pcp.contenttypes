# -*- coding: UTF-8 -*-
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from zope.publisher.browser import BrowserView


class RelationsHelper(BrowserView):

    def uuids_to_contentlisting(self, uuids):
        if not uuids:
            return []
        if not isinstance(uuids, (list, tuple)):
            uuids = [uuids]
        return IContentListing(api.content.find(UID=uuids))
