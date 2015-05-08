"""Definition of the Service content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IService
from pcp.contenttypes.config import PROJECTNAME

ServiceSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ServiceSchema,
    folderish=True,
    moveDiscussion=False
)


class Service(folder.ATFolder):
    """A service managed by this site."""
    implements(IService)

    meta_type = "Service"
    schema = ServiceSchema


atapi.registerType(Service, PROJECTNAME)
