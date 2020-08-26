# -*- coding: utf-8 -*-
from operator import itemgetter
from plone import api
from plone.app.textfield.interfaces import IRichText
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile.interfaces import INamedFileField
from plone.namedfile.interfaces import INamedImageField
from plone.restapi.interfaces import IJsonCompatible
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.dxfields import DefaultFieldSerializer
from Products.Five import BrowserView
from z3c.relationfield.interfaces import IRelationValue
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import noLongerProvides

import base64
import json
import logging

logger = logging.getLogger(__name__)


class ExportRestapi(BrowserView):

    QUERY = {}
    DROP_PATHS = []

    def __call__(self, portal_type=None, include_blobs=False):
        self.portal_type = portal_type
        if not self.request.form.get('form.submitted', False) or not self.portal_type:
            return self.index()

        data = self.export_content(include_blobs=include_blobs)
        number = len(data)
        msg = u'Exported {} {}'.format(number, self.portal_type)
        logger.info(msg)
        data = json.dumps(data, sort_keys=True, indent=4)
        response = self.request.response
        response.setHeader('content-type', 'application/json')
        response.setHeader('content-length', len(data))
        response.setHeader(
            'content-disposition',
            'attachment; filename="{0}.json"'.format(self.portal_type))
        return response.write(data)

    def export_content(self, include_blobs=False):
        data = []
        query = {'portal_type': self.portal_type, 'Language': 'all'}
        # custom setting per type
        query.update(self.QUERY.get(self.portal_type, {}))
        brains = api.content.find(**query)
        logger.info(u'Exporting {} {}'.format(len(brains), self.portal_type))

        if not include_blobs:
            # remove browserlayer to skip finding the custom serializer
            noLongerProvides(self.request, IThemeSpecific)

        for index, brain in enumerate(brains, start=1):
            skip = False
            for drop in self.DROP_PATHS:
                if drop in brain.getPath():
                    skip = True

            if skip:
                continue

            if not index % 100:
                logger.info(u'Handled {} items...'.format(index))
            obj = brain.getObject()
            try:
                serializer = getMultiAdapter((obj, self.request), ISerializeToJson)
                item = serializer()
                data.append(item)
            except Exception as e:
                logger.info(e)

        if not include_blobs:
            # restore browserlayer
            alsoProvides(self.request, IThemeSpecific)

        return data

    def portal_types(self):
        """A list with info on all content types with existing items.
        """
        catalog = api.portal.get_tool('portal_catalog')
        portal_types = api.portal.get_tool('portal_types')
        results = []
        for fti in portal_types.listTypeInfo():
            number = len(catalog(portal_type=fti.id, Language='all'))
            if number >= 1:
                results.append({
                    'number': number,
                    'value': fti.id,
                    'title': translate(
                        fti.title, domain='plone', context=self.request)
                })
        return sorted(results, key=itemgetter('title'))


# make sure the adapter is more specific than the default from restapi
@adapter(INamedImageField, IDexterityContainer, Interface)
class ImageFieldSerializerWithBlobs(DefaultFieldSerializer):
    def __call__(self):
        image = self.field.get(self.context)
        if not image:
            return None
        result = {
            "filename": image.filename,
            "content-type": image.contentType,
            "data":  base64.b64encode(image.data),
            "encoding": "base64",
        }
        return json_compatible(result)


@adapter(INamedFileField, IDexterityContainer, Interface)
class FileFieldSerializerWithBlobs(DefaultFieldSerializer):
    def __call__(self):
        namedfile = self.field.get(self.context)
        if namedfile is None:
            return None

        result = {
            "filename": namedfile.filename,
            "content-type": namedfile.contentType,
            "data": base64.b64encode(namedfile.data),
            "encoding": "base64",
        }
        return json_compatible(result)


@adapter(IRichText, IDexterityContainer, Interface)
class RichttextFieldSerializerWithRawText(DefaultFieldSerializer):
    def __call__(self):
        value = self.get_value()
        if value:
            output = value.raw
            return {
                u"data": json_compatible(output),
                u"content-type": json_compatible(value.mimeType),
                u"encoding": json_compatible(value.encoding),
            }


@adapter(IRelationValue)
@implementer(IJsonCompatible)
def relationvalue_converter_uuid(value):
    if value.to_object:
        return value.to_object.UID()
