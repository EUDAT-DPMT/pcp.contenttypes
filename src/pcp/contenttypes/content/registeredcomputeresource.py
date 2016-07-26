"""Definition of the RegisteredComputeResource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredComputeResource
from pcp.contenttypes.config import PROJECTNAME

RegisteredComputeResourceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredComputeResourceSchema, moveDiscussion=False)


class RegisteredComputeResource(base.ATCTContent):
    """A provisioned physical or virtual server"""
    implements(IRegisteredComputeResource)

    meta_type = "RegisteredComputeResource"
    schema = RegisteredComputeResourceSchema


atapi.registerType(RegisteredComputeResource, PROJECTNAME)
