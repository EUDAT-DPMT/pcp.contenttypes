"""Definition of the RegisteredStorageResource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredStorageResource
from pcp.contenttypes.config import PROJECTNAME

RegisteredStorageResourceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredStorageResourceSchema, moveDiscussion=False)


class RegisteredStorageResource(base.ATCTContent):
    """A provisioned storage space of a certain type"""
    implements(IRegisteredStorageResource)

    meta_type = "RegisteredStorageResource"
    schema = RegisteredStorageResourceSchema


atapi.registerType(RegisteredStorageResource, PROJECTNAME)
