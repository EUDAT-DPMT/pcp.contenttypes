# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer

class IServiceComponentRequest(model.Schema):
    """Dexterity Schema for Providers
    """

    service_component = RelationChoice(
        title=u"Service component",
        description=u"The service component being requested",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service_component",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"], #Actually, it should allows the ServiceComponent type, but it has not been ported to Dexterity yet. 
            "basePath": make_relation_root_path,
        },
    )

    implementations = RelationList(
        title=u"Implementation",
        description=u"If only certain implementations are acceptable, this can be specified here. Leave empty if any implementation is fine.",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "implementations",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["person_dx"], #Actually, it should allows the ServiceComponentImplementation type, but it has not been ported to Dexterity yet.
            "basePath": make_relation_root_path,
        },
    )

    service_hours = RelationChoice(
        title=u"Service hours",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service_hours",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )

# CommentField resource_comment


@implementer(IServiceComponentRequest)
class ServiceComponentRequest(Container):
    """ServiceComponentRequest instance"""
