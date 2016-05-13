"""Definition of the Service Details content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceDetails
from pcp.contenttypes.config import PROJECTNAME

ServiceDetailsSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ServiceDetailsSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceDetails(folder.ATFolder):
    """Detailed information about a service"""
    implements(IServiceDetails)

    meta_type = "ServiceDetails"
    schema = ServiceDetailsSchema


atapi.registerType(ServiceDetails, PROJECTNAME)
