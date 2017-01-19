from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """ DPMT settings """

    accounting_url = schema.TextLine(
        title=u'Connection accounting server',
        description=u'Use http://username:password@host:port/path/to/domain where username+password represent a Manager account on the accounting server',
        default=u'http://accounting.eudat.eu',
        required=True
    )
