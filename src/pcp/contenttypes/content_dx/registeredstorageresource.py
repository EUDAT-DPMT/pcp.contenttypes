# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pcp.contenttypes.content_dx.accountable import Accountable
from pcp.contenttypes.content_dx.common import CommonUtilities
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class ISize(Interface):

    value = schema.TextLine(
        title=u'Value',
        required=False,
    )

    unit = schema.Choice(
        title=u'Unit',
        vocabulary='dpmt.information_units',
        required=False,
    )

    storage_class = schema.Choice(
        title=u'Storage class',
        vocabulary='dpmt.storage_types',
        required=False,
    )


class IRegisteredStorageResource(model.Schema):
    """Dexterity Schema for Registered Storage Resources
    """
    size = schema.List(
        title=u'Size',
        description=u'Maximal size and type of this storage resource',
        value_type=DictRow(title=u'Foo', schema=ISize),
        default=[{'value': None, 'unit': None, 'storage_class': None}],
        required=False,
    )
    directives.widget(
        'size',
        DataGridFieldFactory,
        auto_append=False,
        allow_insert=False,
    )

    # RecordField size
    # ComputedField usage
    # ComputedField number
    # ComputedField allocated
    # ComputedField storage_class

    max_objects = schema.Int(
        title=u"Max. Objects",
        description=u"Allocated (maximum) number of objects",
        required=False,
    )

    cost_factor = schema.Float(title=u"Cost factor", required=False,)

    preserve_until = schema.Datetime(
        title=u"Preserve until",
        description=u"Until when does this resource need to be allocated?",
        required=False,
    )


@implementer(IRegisteredStorageResource)
class RegisteredStorageResource(Container, CommonUtilities, Accountable):
    """RegisteredStorageResource instance"""
