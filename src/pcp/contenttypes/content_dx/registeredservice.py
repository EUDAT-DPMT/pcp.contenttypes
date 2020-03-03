# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IRegisteredService(model.Schema):
    """Dexterity Schema for Registered services
    """

    #ReferenceField general_provider
    #ReferenceField contact
    #ReferenceField managers

    monitored = schema.Bool(
            title=u'Monitored',
            description=u'Should this service be monitored?',
            required=False,
            )

    #ReferenceField service_components
    #ReferenceField original_request
    #ComputedField registry_link
    #BackReferenceField used_by_projects
    #ComputedField scopes
    #BackReferenceField resources

@implementer(IRegisteredService)
class RegisteredService(Container):
    """RegisteredService instance"""
