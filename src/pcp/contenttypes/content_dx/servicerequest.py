# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IServiceRequest(model.Schema):
    """Dexterity Schema for ServiceRequest
    """

    # ReferenceField service
    # ReferenceField service_option
    # ReferenceField service_hours
    # BackReferenceField registered_service
    # CommentField resource_comment


@implementer(IServiceRequest)
class ServiceRequest(Container):
    """ServiceRequest instance"""
