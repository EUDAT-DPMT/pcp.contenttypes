# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IService(model.Schema):
    """Dexterity Schema for Services
    """

    dexteritytextindexer.searchable(
        "url",
        "service_area",
        "service_type",
        "value_to_customer",
        "risks",
        "funders_for_service",
        "request_procedures",
    )

    description_internal = schema.TextLine(
        title=u"Internal description", required=False,
    )

    url = schema.URI(title=u"Url", required=False,)

    service_area = schema.TextLine(title=u"Service area", required=False,)

    service_type = schema.TextLine(title=u"Service type", required=False,)

    value_to_customer = schema.TextLine(title=u"Value to customer", required=False,)

    risks = schema.TextLine(title=u"Risks", required=False,)

    funders_for_service = schema.TextLine(
        title=u"Funders", description=u"Funders for this service", required=False,
    )

    request_procedures = schema.TextLine(title=u"Request procedures", required=False,)

    managed_by = RelationChoice(
        title=u"Managed by",
        required=False,
        source=CatalogSource(portal_type=["Person"]),
    )


@implementer(IService)
class Service(Container):
    """Service instance"""
