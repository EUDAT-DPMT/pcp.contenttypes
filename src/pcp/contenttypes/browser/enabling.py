from Products.Five.browser import BrowserView

import plone.api


class Enabling(BrowserView):
    def getServices(self):
        """ For PFG enabling forms ('service' field) """
        catalog = plone.api.portal.get_tool('portal_catalog')
        path = '{}/catalog'.format('/'.join(plone.api.portal.get().getPhysicalPath()))
        query = dict(portal_type='Service', sort_on='sortable_title', path=path)
        result = list()
        for brain in catalog(**query):
            result.append((brain.getId, brain.Title))
        return result

    def getProjects(self):
        """ For PFG enabling forms ('project' field) """
        catalog = plone.api.portal.get_tool('portal_catalog')
        path = '{}/projects'.format('/'.join(plone.api.portal.get().getPhysicalPath()))
        query = dict(portal_type='Project', sort_on='sortable_title', path=path)
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
            has_project = 'project' in form.objectIds()
            has_save_adapter = len(form.objectValues('FormSaveData2ContentAdapter')) > 0
            save_adapter_url = None
            saved_forms = 0
            if has_save_adapter:
                save_adapter = form.objectValues('FormSaveData2ContentAdapter')[0]
                saved_forms = len(save_adapter.objectIds())
                save_adapter_url = save_adapter.absolute_url() + '/folder_contents'
            result.append(
                dict(
                    saved_forms=saved_forms,
                    save_adapter_url=save_adapter_url,
                    has_service=has_service,
                    has_project=has_project,
                    has_save_adapter=has_save_adapter,
                    url=brain.getURL(),
                    title=brain.Title,
                )
            )
        return result

    def process_enabling_form_data(self):

        catalog = plone.api.portal.get_tool('portal_catalog')

        # find associated service
        service_name = self.context.Schema().getField('service').get(self.context)
        path = '{}/catalog'.format('/'.join(plone.api.portal.get().getPhysicalPath()))
        brains = catalog(dict(portal_type='Service', getId=service_name, path=path))
        if not brains:
            raise ValueError(f'Service {service_name} not found')
        service = brains[0].getObject()

        # find associated service
        project_name = self.context.Schema().getField('project').get(self.context)
        path = '{}/projects'.format('/'.join(plone.api.portal.get().getPhysicalPath()))
        brains = catalog(dict(portal_type='Project', getId=project_name, path=path))
        if not brains:
            raise ValueError(f'Project {project_name} not found')
        project = brains[0].getObject()

        # find ActionLists associated with the service
        brains = catalog(dict(portal_type='ActionList'))
        action_lists = [brain.getObject() for brain in brains]
        action_lists = [al for al in action_lists if al.getService() == service]

        filter_method = f'filter_{service_name}'
        method = getattr(self, filter_method, None)
        if not method:
            raise ValueError(
                f'No filtering method {filter_method}() implemented'
            )

        action_lists = method(project, service, action_lists)

        for al in action_lists:
            al.createPOI(target_path='/'.join(project.getPhysicalPath()))

        return 'DONE'

    def filter_B2SAFE(self, project, service, action_lists):
        """ Do some filtering...."""

        return action_lists

    def filter_B2FIND(self, project, service, action_lists):
        """ Do some filtering...."""

        return action_lists

    def filter_B2SHARE(self, project, service, action_lists):
        """ Do some filtering...."""

        return action_lists

    def filter_B2DROP(self, project, service, action_lists):
        """ Do some filtering...."""

        return action_lists

    def filter_B2STAGE(self, project, service, action_lists):
        """ Do some filtering...."""

        return action_lists
