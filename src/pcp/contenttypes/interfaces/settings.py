from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """ DPMT settings """

    accounting_url = schema.TextLine(
        title=u'Connection accounting server',
        description=u'Use http://host:port/path/to/domain',
        default=u'http://accounting.eudat.eu',
        required=True
    )

    accounting_username = schema.TextLine(
        title=u'Username of the manager account on the accounting server',
        default=None
    )

    accounting_password = schema.Password(
        title=u'Password of the manager account on the accounting server',
        default=None
    )
