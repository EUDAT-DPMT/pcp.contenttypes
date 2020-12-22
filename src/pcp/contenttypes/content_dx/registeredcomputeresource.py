# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IRegisteredComputeResource(model.Schema):
    """Dexterity Schema for Registered Compute Resources"""

    dexteritytextindexer.searchable(
        "hostname",
        "ip",
        "cpus",
        "memory",
        "localdisk",
        "virtualization",
        "os",
        "software",
    )

    hostname = schema.TextLine(
        title=u"Hostname",
        required=False,
    )

    ip = schema.TextLine(
        title=u"IP",
        required=False,
    )

    cpus = schema.TextLine(
        title=u"CPUs",
        required=False,
    )

    memory = schema.TextLine(
        title=u"Memory",
        required=False,
    )

    localdisk = schema.TextLine(
        title=u"Local disk",
        required=False,
    )

    virtualization = schema.TextLine(
        title=u"Virtualization",
        required=False,
    )

    os = schema.TextLine(
        title=u"OS",
        required=False,
    )

    software = schema.TextLine(
        title=u"Software",
        required=False,
    )


@implementer(IRegisteredComputeResource)
class RegisteredComputeResource(Container):
    """RegisteredComputeResource instance"""
