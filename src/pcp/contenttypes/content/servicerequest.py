"""Definition of the ServiceRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceRequest
from pcp.contenttypes.config import PROJECTNAME

ServiceRequestSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(ServiceRequestSchema, moveDiscussion=False)


class ServiceRequest(base.ATCTContent):
    """A project requests a service"""
    implements(IServiceRequest)

    meta_type = "ServiceRequest"
    schema = ServiceRequestSchema


atapi.registerType(ServiceRequest, PROJECTNAME)
