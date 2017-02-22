
import plone.api

from Products.Five.browser import BrowserView


class Misc(BrowserView):

    def getServices(self):
        catalog = plone.api.portal.get_tool('portal_catalog')
        query = dict(portal_type='Service', sort_on='sortable_title')
        result = list()
        for brain in catalog(**query):
            result.append((brain.getId, brain.Title))
        return result

    def enabling_forms(self):

        catalog = plone.api.portal.get_tool('portal_catalog')
        query = dict(portal_type='FormFolder')
        result = list()
        for brain in catalog(**query):
            form = brain.getObject()
            has_service = 'service' in form.objectIds()
            has_save_adapter = len(form.objectValues('FormSaveData2ContentAdapter')) > 0
            result.append(dict(
                has_service=has_service,
                has_save_adapter=has_save_adapter,
                url=brain.getURL(),
                title=brain.Title))
        return result
