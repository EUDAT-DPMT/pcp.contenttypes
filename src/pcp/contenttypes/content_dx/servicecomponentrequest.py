# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IServiceComponentRequest(model.Schema):
    """Dexterity Schema for Providers
    """


# ReferenceField service_component
# ReferenceField implementations
# ReferenceField service_hours
# CommentField resource_comment


@implementer(IServiceComponentRequest)
class ServiceComponentRequest(Container):
    """ServiceComponentRequest instance"""
