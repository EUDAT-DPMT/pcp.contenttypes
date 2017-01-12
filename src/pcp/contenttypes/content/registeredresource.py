"""Definition of the RegisteredResource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredResource
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import CommonUtilities

RegisteredResourceSchema = schemata.ATContentTypeSchema.copy() + ResourceFields.copy() \
    + atapi.Schema((

        # -*- Your Archetypes field definitions here ... -*-

    ))


schemata.finalizeATCTSchema(RegisteredResourceSchema, moveDiscussion=False)


class RegisteredResource(base.ATCTContent, CommonUtilities):
    """A CDI admin registers a new resource"""
    implements(IRegisteredResource)

    meta_type = "RegisteredResource"
    schema = RegisteredResourceSchema


atapi.registerType(RegisteredResource, PROJECTNAME)
