# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IRegisteredStorageResource(model.Schema):
    """Dexterity Schema for Registered Storage Resources
    """

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
class RegisteredStorageResource(Container):
    """RegisteredStorageResource instance"""
