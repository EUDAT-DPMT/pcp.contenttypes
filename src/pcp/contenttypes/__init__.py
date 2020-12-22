from plone.app.upgrade.utils import alias_module
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface


# Define a message factory for when this product is internationalised.
# This will be imported with the special name "_" in most modules. Strings
# like _(u"message") will then be extracted by i18n tools for translation.

contenttypesMessageFactory = MessageFactory('pcp.contenttypes')

zodbupdate_rename_dict = {
    'webdav.EtagSupport EtagSupport': 'OFS.EtagSupport EtagSupport',
    'webdav.EtagSupport EtagBaseInterface': 'OFS.EtagSupport EtagBaseInterface',
}


class IBBB(Interface):
    pass


# stuff from incompletely uninstalled addons
try:
    from collective.handleclient.interfaces import ICollectiveHandleclientLayer

    ICollectiveHandleclientLayer  # noqa
except ImportError:
    alias_module(
        'collective.handleclient.interfaces.ICollectiveHandleclientLayer', IBBB
    )

try:
    from App.interfaces import IPersistentExtra

    IPersistentExtra  # noqa
except ImportError:
    alias_module('App.interfaces.IPersistentExtra', IBBB)

try:
    from App.interfaces import IUndoSupport

    IUndoSupport  # noqa
except ImportError:
    alias_module('App.interfaces.IUndoSupport', IBBB)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
