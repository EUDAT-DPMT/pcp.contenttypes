"""Definition of the Resource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IResource
from pcp.contenttypes.config import PROJECTNAME

ResourceSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ResourceSchema,
    folderish=True,
    moveDiscussion=False
)


class Resource(folder.ATFolder):
    """A resource needed to provide a service managed by a project on this site."""
    implements(IResource)

    meta_type = "Resource"
    schema = ResourceSchema


atapi.registerType(Resource, PROJECTNAME)
