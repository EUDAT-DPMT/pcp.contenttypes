"""Definition of the ServiceComponentRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponentRequest
from pcp.contenttypes.config import PROJECTNAME

ServiceComponentRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(ServiceComponentRequestSchema, moveDiscussion=False)


class ServiceComponentRequest(folder.ATFolder):
    """A project requests a specific service component"""
    implements(IServiceComponentRequest)

    meta_type = "ServiceComponentRequest"
    schema = ServiceComponentRequestSchema


atapi.registerType(ServiceComponentRequest, PROJECTNAME)
