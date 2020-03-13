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


class ICommunity(model.Schema):
    """Dexterity Schema for Communities
    """

    dexteritytextindexer.searchable("VAT")

    url = schema.URI(title=u"Url", required=False,)

    # AddressField address

    VAT = schema.TextLine(title=u"VAT", required=False,)

    representative = RelationChoice(
        title=u"Representative",
        description=u"Main person representing the Customer.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "representative",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    admins = RelationList(
        title=u"Administrators",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "admins",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    # BackReferenceField affiliated

    # BackReferenceField projects_involved

    # BackReferenceField primary_provider

    # BackReferenceField secondary_provider

    topics = schema.TextLine(
        title=u"Topics",
        description=u"If applicable, please mention the scientific field(s) this customer is focussing on.",
        required=False,
    )

    # BackReferenceField resources

    # ComputedField usage_summary

    # ComputedField resource_usage


@implementer(ICommunity)
class Community(Container):
    """Community instance"""
