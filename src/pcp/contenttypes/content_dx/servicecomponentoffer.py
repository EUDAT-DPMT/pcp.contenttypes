# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IServiceComponentOffer(model.Schema):
    """Dexterity Schema for ServiceComponentOffer
    """

    # ReferenceField service_component
    # ReferenceField implementations
    # ReferenceField slas


@implementer(IServiceComponentOffer)
class ServiceComponentOffer(Container):
    """ServiceComponentOffer instance"""
