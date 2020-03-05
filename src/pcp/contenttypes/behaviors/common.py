"""Common behaviours for DPMT content types.

Includes form fields and behaviour adapters that are useful
throughout the application
"""
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider



# parts for the data grid type fields
class IIdentifierRowSchema(Interface):

    type = schema.Choice(
        title=u"Identifier Type",
        vocabulary='dpmt.identifier_types',
        required=False,
        )

    value = schema.TextLine(
        title=u"Identifier Value",
        required=False,
        )


class IAdditionalRowSchema(Interface):

    key = schema.TextLine(
        title=u"Key",
        required=True,
        )

    value = schema.TextLine(
        title=u"Value",
        required=True,
        )


@provider(IFormFieldProvider)
class IDPMTCommon(model.Schema):
    """Add fields shared by most content types
    """

    fieldset(
        'details',
        label=u'Details',
        fields=('uid', 'identifiers', 'additional'),
    )

    uid = schema.TextLine(
        title=u"UID",
        description=u"The application internal UID",
        required=False,
        # allow_uncommon=True,  # what's this?
    )
    directives.mode(uid='display')

    identifiers = schema.List(
        title=u"Identifiers",
        description=u"Further identifiers for this item",
        value_type=DictRow(title=u"Identifier", schema=IIdentifierRowSchema),
        required=False,
        missing_value=[],
    )
    directives.widget('identifiers', DataGridFieldFactory)

    additional = schema.List(
        title=u"Additional Properties",
        description=u"Further key/value pairs describing this item",
        value_type=DictRow(title=u"Additional Property",
                           schema=IAdditionalRowSchema),
        required=False,
        missing_value=[],
    )
    directives.widget('additional', DataGridFieldFactory)


@implementer(IDPMTCommon)
@adapter(IDexterityContent)
class DPMTCommon(object):
    """Support for computed fields and controlled vocabularies(?)
    """

    def __init__(self, context):
        self.context = context

    @property
    def uid(self):
        return IUUID(self.context, None)

    @uid.setter
    def uid(self, value):
        pass

    def _get_identifiers(self):
        return self.context.identifiers

    def _set_identifiers(self, value):
        self.context.identifiers = value

    identifiers = property(_get_identifiers, _set_identifiers)

    def _get_additional(self):
        return self.context.additional

    def _set_additional(self, value):
        self.context.additional = value

    additional = property(_get_additional, _set_additional)


class IDPMTCommonMarker(Interface):
    """Marker interface that will be provided by instances using the
    IDPMTCommon behavior.
    """
