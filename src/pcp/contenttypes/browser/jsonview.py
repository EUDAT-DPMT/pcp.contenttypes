# Inspired by
# http://opensourcehacker.com/2013/01/04/exporting-plone-content-as-json/
# Thanks Mikko!

#
# for DX types use Plone's restapi (wasn't available before)
#

from zope.component import getMultiAdapter
from plone.restapi.interfaces import ISerializeToJson

import os
import base64

import json

import plone.api
from Products.Five.browser import BrowserView
from Products.CMFCore.interfaces import IFolderish
from plone.app.blob.interfaces import IBlobWrapper
from DateTime import DateTime

from Products.Archetypes.atapi import ReferenceField
from Products.ATExtensions.ateapi import FormattableName

#: Private attributes we add to the export list
EXPORT_ATTRIBUTES = ["portal_type", "id"]

#: Do we dump out binary data... default we do, but can be controlled with env var
EXPORT_BINARY = os.getenv("EXPORT_BINARY", None)
if EXPORT_BINARY:
    EXPORT_BINARY = EXPORT_BINARY == "true"
else:
    EXPORT_BINARY = False


hidden_fields = (
    'constrainTypesMode',
    'locallyAllowedTypes',
    'immediatelyAddableTypes',
    'location',
    'language',
    'effectiveDate',
    'creation_date',
    'modification_date',
    'creators',
    'excludeFromNav',
    'nextPreviousEnabled'
)


class JSONViewDX(BrowserView):
    """Present dexterity types as JSON"""

    def serialize(self):
        serializer = getMultiAdapter((self.context, self.request), ISerializeToJson)
        data = serializer()
        pretty = json.dumps(data, sort_keys=True, indent=4)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty



class JSONView(BrowserView):
    """Present Archetypes-based content as JSON"""

    @property
    def include_all(self):
        return 'include_all' in self.request.form

    @property
    def url_tool(self):
        return plone.api.portal.get_tool('portal_url')

    def handle_client(self):
        return plone.api.portal.get_tool('handle_client')

    def convert(self, value):
        """
        Convert value to more JSON friendly format.
        """
        if isinstance(value, DateTime):
            # Zope DateTime
            # http://pypi.python.org/pypi/DateTime/3.0.2
            return value.ISO8601()
        elif isinstance(value, FormattableName):
            return dict(value.items())
        elif IBlobWrapper.providedBy(value):
            # TODO: equivalent handling of binary data as in isBinary special case
            return None
        elif hasattr(value, "isBinary") and value.isBinary():

            if not EXPORT_BINARY:
                return None

            # Archetypes FileField and ImageField payloads
            # are binary as OFS.Image.File object
            data = getattr(value.data, "data", None)
            if not data:
                return None
            return base64.b64encode(data)
        else:
            # Passthrough
            return value

    def fieldData(self, context):
        data = {}
        for field in context.Schema().viewableFields(context):

            name = field.getName()

            if not self.include_all:
                # content class specific hidding of AT Fields
                hidden_json_fields = getattr(context, 'hidden_json_fields', ())
                if name in hidden_json_fields:
                    continue

                # global blacklist
                if name in hidden_fields:
                    continue

            if isinstance(field, ReferenceField):
                value = []
                objs = field.get(context, aslist=True)
                uids = field.getRaw(context, aslist=True)
                for o, u in zip(objs, uids):
                    d = {}
                    d['uid'] = u
                    d['title'] = o.Title()
                    d['path'] = '/'.join(self.url_tool.getRelativeContentPath(o))
                    if self.handle_client() is not None:
                        handle = self.handle_client()._getHandle(o)
                        if handle:
                            d['handle'] = handle
                    value.append(d)
            else:
                try:
                    value = field.getRaw(context)
                except AttributeError:   # happens for computed fields
                    value = field.get(context)
            data[name] = self.convert(value)
        return data

    def attributeData(self, context):
        data = {}
        for key in EXPORT_ATTRIBUTES:
            data[key] = self.convert(getattr(context, key, None))
        return data

    def export(self, context, recursive=False):
        """Export fields and selected attributes"""

        data = self.fieldData(context)
        data.update(self.attributeData(context))

        if recursive and IFolderish.providedBy(context):
            children = []
            for obj in context.listFolderContents():
                children.append(self.export(obj, True))
            data['children'] = children

        return [data]

    def json_view(self, recursive=False):
        """AT-based content as JSON"""

        context = self.context.aq_inner
        data = self.export(context, recursive=recursive)
        pretty = json.dumps(data, sort_keys=True, indent=4)
        self.request.response.setHeader("Content-type", "application/json")
        return pretty
