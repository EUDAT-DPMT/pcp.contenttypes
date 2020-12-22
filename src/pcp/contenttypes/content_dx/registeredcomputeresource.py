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
        'hostname',
        'ip',
        'cpus',
        'memory',
        'localdisk',
        'virtualization',
        'os',
        'software',
    )

    hostname = schema.TextLine(
        title='Hostname',
        required=False,
    )

    ip = schema.TextLine(
        title='IP',
        required=False,
    )

    cpus = schema.TextLine(
        title='CPUs',
        required=False,
    )

    memory = schema.TextLine(
        title='Memory',
        required=False,
    )

    localdisk = schema.TextLine(
        title='Local disk',
        required=False,
    )

    virtualization = schema.TextLine(
        title='Virtualization',
        required=False,
    )

    os = schema.TextLine(
        title='OS',
        required=False,
    )

    software = schema.TextLine(
        title='Software',
        required=False,
    )


@implementer(IRegisteredComputeResource)
class RegisteredComputeResource(Container):
    """RegisteredComputeResource instance"""
