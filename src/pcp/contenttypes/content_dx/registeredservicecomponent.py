# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IRegisteredServiceComponent(model.Schema):
    """Dexterity Schema for Registered Service Component
    """

    dexteritytextindexer.searchable(
        "service_type",
        "service_url",
        "host_name",
        "host_dn",
        "host_os",
        "host_architecture",
        "emergency_phone",
        "alarm_email",
        "helpdesk_email",
        "supported_os",
    )

    # ReferenceField service_component_implementation_details
    # ReferenceField service_providers
    # ReferenceField contacts

    service_type = schema.TextLine(title=u"Service component type", required=False,)

    service_url = schema.TextLine(
        title=u"Service URL",
        description=u"[http|https|irods|gsiftp|ssh]://URL:port",
        required=False,
    )

    # BackReferenceField parent_services
    # ComputedField scopes

    host_name = schema.TextLine(
        title=u"Host name",
        description=u"In valid FQDN format (fully qualified domain name)",
        required=False,
    )

    host_ip4 = schema.TextLine(
        title=u"IP4 address",
        description=u"Host's IP4 address (a.b.c.d)",
        required=False,
    )

    host_ip6 = schema.TextLine(
        title=u"IP6 address",
        description=u"Host's IP6 address (0000:0000:0000:0000:0000:0000:0000:0000[/int]) (optional [/int] range)))",
        required=False,
    )

    host_dn = schema.TextLine(
        title=u"Distinguished name (DN)",
        description=u"Host's DN (/C=.../OU=...?...)",
        required=False,
    )

    host_os = schema.TextLine(
        title=u"Host operating system",
        description=u"Alphanumeric and basic punctuation",
        required=False,
    )

    host_architecture = schema.TextLine(
        title=u"Host_architecture",
        description=u"Alphanumeric and basic punctuation",
        required=False,
    )

    monitored = schema.Bool(title=u"Monitored", required=False,)

    # ComputedField registrylink
    # RecordsField implementation_configuration
    # BackReferenceField resources


@implementer(IRegisteredServiceComponent)
class RegisteredServiceComponent(Container):
    """RegisteredServiceComponent instance"""
