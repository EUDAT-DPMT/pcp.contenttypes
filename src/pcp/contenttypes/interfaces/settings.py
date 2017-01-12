from zope import schema
from zope.interface import Interface


class ISettings(Interface):
    """ DPMT settings """

    accounting_url = schema.TextLine(
        title=u'Connection accounting server',
        default=u'http://accounting.eudat.eu',
        required=True
    )
