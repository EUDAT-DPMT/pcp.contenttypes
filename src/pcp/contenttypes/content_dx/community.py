# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class ICommunity(model.Schema):
    """Dexterity Schema for Communities
    """

    dexteritytextindexer.searchable("VAT")

    url = schema.URI(title=u"Url", required=False,)

    # AddressField address

    VAT = schema.TextLine(title=u"VAT", required=False,)

    # ReferenceField representative

    # ReferenceField admins

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
