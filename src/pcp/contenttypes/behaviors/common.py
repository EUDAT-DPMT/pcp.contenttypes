"""Common behaviours for DPMT content types.

Includes form fields and behaviour adapters that are useful 
throughout the application 
"""

from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider

from plone.uuid.interfaces import IUUID


@provider(IFormFieldProvider)
class IDPMTCommon(model.Schema):
    """Add fields shared by most content types
    """

    directives.fieldset(
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

    identifiers = schema.Tuple(
        title=u"Identifiers",
        description=u"Further identifiers for this item",
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )

    additional = schema.Tuple(
        title=u"Additional Properties",
        description=u"Further key/value pairs describing this item",
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


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
        return self.context.identifiers or []
        
    def _set_identifiers(self, value):
        self.context.identifiers = value
        
    identifiers = property(_get_identifiers, _set_identifiers)

    def _get_additional(self):
        return self.context.additional or []
        
    def _set_additional(self, value):
        self.context.additional = value
        
    additional = property(_get_additional, _set_additional)


class IDPMTCommonMarker(Interface):
    """Marker interface that will be provided by instances using the
    IDPMTCommon behavior. 
    """
