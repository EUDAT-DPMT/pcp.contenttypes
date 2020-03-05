# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IResourceOffer(model.Schema):
    """Dexterity Schema for ResourceOffer
    """


@implementer(IResourceOffer)
class ResourceOffer(Container):
    """ResourceOffer instance"""
