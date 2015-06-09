"""Definition of the Provider content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.config import PROJECTNAME

ProviderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ProviderSchema,
    folderish=True,
    moveDiscussion=False
)


class Provider(folder.ATFolder):
    """Compute or data service provider"""
    implements(IProvider)

    meta_type = "Provider"
    schema = ProviderSchema


atapi.registerType(Provider, PROJECTNAME)
