# -*- coding: UTF-8 -*-
from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """ DPMT settings """

    accounting_url = schema.TextLine(
        title=u'Connection accounting server',
        description=u'Use http://host:port/path/to/domain',
        default=u'http://accounting.eudat.eu',
        required=True,
    )

    accounting_username = schema.TextLine(
        title=u'Username of the manager account on the accounting server',
        default=None,
    )

    accounting_password = schema.Password(
        title=u'Password of the manager account on the accounting server',
        default=None,
    )

    identifier_types = schema.List(
        title=u'Identifiers',
        description=u"Types of identifiers used to refer items.",
        required=False,
        default=[
            u'handle',
            u'doi',
            u'epic',
            u'orcid',
            u'rct_uid',
            u'dmp_online',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )

    operating_systems = schema.List(
        title=u'Operating Systems',
        required=False,
        default=[
            u'SLES - SuSE Linux Enterprise Server from Novell',
            u'RHEL - Red Hat Enterprise Linux from Red Hat',
            u'Ubuntu - Ubuntu Server from Canonical',
            u'SL - Scientific Linux',
            u'Debian - Debian',
            u'CentOS - The Community Enterprise Operating System',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )

    storage_types = schema.List(
        title=u'Storage types',
        required=False,
        default=[
            u'online',
            u'nearline',
            u'offline',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )

    provider_types = schema.List(
        title=u'Provider Types',
        required=False,
        default=[
            u'generic',
            u'thematic',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )

    provider_stati = schema.List(
        title=u'Provider Stati',
        required=False,
        default=[
            u'candidate',
            u'certified',
            u'closed',
            u'deprecated',
            u'suspended',
            u'uncertified',
        ],
        missing_value=[],
        value_type=schema.TextLine(),
    )
