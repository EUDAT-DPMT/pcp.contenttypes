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


class IServiceComponentOffer(model.Schema):
    """Dexterity Schema for ServiceComponentOffer
    """

    service_component = RelationChoice(
        title=u"Service component offered",
        description=u"Reference to the catalog entry of the service component being offered.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service_component",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"], #Actually ServiceComponent 
            "basePath": make_relation_root_path,
        },
    )   

    implementations = RelationList(
        title=u"Implementations offered",
        description=u"Reference to the catalog entry of the implementations(s) of the service component being offered.",
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
            "selectableTypes": ["person_dx"], #Actually ServiceComponentImplementation
            "basePath": make_relation_root_path,
        },
    )   

    slas= RelationList(
        title=u"SLAs/OLAs offered",
        description=u"Potential Service/Operational Level Agreements under which the service component is being offered.",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "slas",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )


@implementer(IServiceComponentOffer)
class ServiceComponentOffer(Container):
    """ServiceComponentOffer instance"""
