
import plone.api

from Products.Five.browser import BrowserView


class Enabling(BrowserView):

    def getServices(self):
        """ For PFG enabling forms ('service' field) """
        catalog = plone.api.portal.get_tool('portal_catalog')
        query = dict(portal_type='Service', sort_on='sortable_title')
        result = list()
        for brain in catalog(**query):
            result.append((brain.getId, brain.Title))
        return result

    def enabling_forms(self):
        """ Initial enabling form """
        catalog = plone.api.portal.get_tool('portal_catalog')
        query = dict(portal_type='FormFolder')
        result = list()
        for brain in catalog(**query):
            form = brain.getObject()
            has_service = 'service' in form.objectIds()
            has_save_adapter = len(form.objectValues('FormSaveData2ContentAdapter')) > 0
            save_adapter_url = None
            saved_forms = 0
            if has_save_adapter:
                save_adapter = form.objectValues('FormSaveData2ContentAdapter')[0]
                saved_forms = len(save_adapter.objectIds())
                save_adapter_url = save_adapter.absolute_url() + '/folder_contents'
            result.append(dict(
                saved_forms=saved_forms,
                save_adapter_url=save_adapter_url,
                has_service=has_service,
                has_save_adapter=has_save_adapter,
                url=brain.getURL(),
                title=brain.Title))
        return result
