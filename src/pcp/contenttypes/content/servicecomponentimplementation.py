"""Definition of the ServiceComponentImplementation content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponentImplementation
from pcp.contenttypes.config import PROJECTNAME

ServiceComponentImplementationSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ServiceComponentImplementationSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponentImplementation(folder.ATFolder):
    """Specific implementation of a service component"""
    implements(IServiceComponentImplementation)

    meta_type = "ServiceComponentImplementation"
    schema = ServiceComponentImplementationSchema


atapi.registerType(ServiceComponentImplementation, PROJECTNAME)
