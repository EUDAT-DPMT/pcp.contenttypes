from datetime import datetime
from DateTime import DateTime
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.restapi.interfaces import IDeserializeFromJson
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from ZPublisher.HTTPRequest import FileUpload

import json
import logging
import transaction


logger = logging.getLogger(__name__)

CONFIG = {
    'endpoint_handle': {'container': None},
}

BUGS = {}

DROP_FIELDS = []

DEFAULTS = {}

DROP_PATHS = []


class ImportForm(BrowserView):
    def __call__(self, jsonfile=None):
        if jsonfile:
            self.portal_type = jsonfile.filename.split('.json')[0]
            self.portal = api.portal.get()
            self.fti = getUtility(IDexterityFTI, name=self.portal_type)
            status = 'success'
            try:
                if isinstance(jsonfile, str):
                    return_json = True
                    data = json.loads(jsonfile)
                elif isinstance(jsonfile, FileUpload):
                    data = json.loads(jsonfile.read())
                else:
                    raise ('Data is neither text nor upload.')
            except Exception as e:
                logger.error(e)
                status = 'error'
                msg = e
                api.portal.show_message(
                    f'Fehler beim Dateiuplad: {e}', request=self.request,
                )
            else:
                msg = self.do_import(data)
                api.portal.show_message(msg, self.request)

        return self.index()

    def do_import(self, data):
        start = datetime.now()
        # self.remove_old_content()
        added = self.import_new_content(data)
        transaction.commit()
        end = datetime.now()
        delta = end - start
        msg = 'Imported {} {} in {} seconds'.format(
            len(added), self.portal_type, delta.seconds,
        )
        logger.info(msg)
        return msg

    def remove_old_content(self):
        removed = []
        for brain in api.content.find(portal_type=self.portal_type):
            # remove only changed or dropped items
            obj = brain.getObject()
            api.content.delete(obj=obj, check_linkintegrity=False)

    def import_new_content(self, data):
        added = []
        container = None
        container_path = CONFIG.get(self.portal_type, {}).get('container', None)
        if container_path:
            container = api.content.get(path=container_path)
            if not container:
                raise RuntimeError(
                    f'Target folder {container_path} for type {self.portal_type} is missing'
                )
        for index, item in enumerate(data, start=1):
            skip = False
            for drop in DROP_PATHS:
                if drop in item['@id']:
                    skip = True
            if skip:
                continue

            if not index % 100:
                logger.info(f'Imported {index} items...')

            new_id = item['id']
            uuid = item['UID']
            item = self.handle_broken(item)
            item = self.handle_dropped(item)
            item = self.global_dict_modifier(item)
            item = self.custom_dict_modifier(item)

            container = self.handle_container(item) or container
            if not container:
                logger.info(f'No container found for {item["@id"]}')
                continue

            if new_id in container:
                logger.info(f'{new_id} already exists')
                continue

            container.invokeFactory(self.portal_type, item['id'])
            new = container[item['id']]

            # import using plone.restapi deserializers
            deserializer = getMultiAdapter((new, self.request), IDeserializeFromJson)
            new = deserializer(validate_all=False, data=item)

            if api.content.find(UID=uuid):
                logger.warn(
                    'UID {} of {} already in use by {}'.format(
                        uuid, item['id'], api.content.get(UID=uuid).absolute_url(),
                    ),
                )
            else:
                setattr(new, '_plone.uuid', uuid)
                new.reindexObject(idxs=['UID'])

            if item['review_state'] == 'published':
                api.content.transition(to_state='published', obj=new)
            self.custom_modifier(new)

            # set date as last step
            modified = datetime.strptime(item['modified'], '%Y-%m-%dT%H:%M:%S%z')
            new.modification_date = DateTime(modified)
            new.reindexObject(idxs=['modified'])
            logger.info(f'Created {self.portal_type} {new.absolute_url()}')
            added.append(new.absolute_url())
        return added

    def handle_broken(self, item):
        """Fix some invalid values."""
        if item['id'] not in BUGS:
            return item
        for key, value in BUGS[item['id']].items():
            logger.info(
                f'Replaced {item[key]} with {value} for field {key} of {item["id"]}'
            )
            item[key] = value
        return item

    def handle_dropped(self, item):
        """Drop some fields, especially relations."""
        for key in DROP_FIELDS:
            item.pop(key, None)
        return item

    def handle_defaults(self, item):
        """Set missing values especially for required fields."""
        for key in DEFAULTS:
            if not item.get(key, None):
                item[key] = DEFAULTS[key]
        return item

    def global_dict_modifier(self, item):
        return item

    def custom_dict_modifier(self, item):
        modifier = getattr(
            self, f'fixup_{self.portal_type.lower().replace(".", "_")}_dict', None
        )
        if modifier and callable(modifier):
            item = modifier(item)
        return item

    def custom_modifier(self, obj):
        modifier = getattr(self, f'fixup_{self.portal_type.lower().replace(".", "_")}', None)
        if modifier and callable(modifier):
            modifier(obj)

    def handle_container(self, item):
        method = getattr(self, f'handle_{self.portal_type.lower().replace(".", "_")}_container', None)
        if method and callable(method):
            return method(item)

    def handle_endpoint_handle_container(self, item):
        return self.get_parent_as_container(item)

    def handle_endpoint_irods_container(self, item):
        return self.get_parent_as_container(item)

    def get_parent_as_container(self, item):
        parent_url = item['parent']['@id']
        parent_path = '/'.join(parent_url.split('/')[4:])
        parent_path = '/' + parent_path
        parent = api.content.get(path=parent_path)
        if parent:
            return parent
        else:
            logger.info(f'No Parent found for {item["@id"]}')
