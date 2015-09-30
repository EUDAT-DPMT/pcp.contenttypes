"""Definition of the RegisteredService content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.config import PROJECTNAME

RegisteredServiceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredServiceSchema, moveDiscussion=False)


class RegisteredService(base.ATCTContent):
    """A CDI admin registers a new service"""
    implements(IRegisteredService)

    meta_type = "RegisteredService"
    schema = RegisteredServiceSchema


atapi.registerType(RegisteredService, PROJECTNAME)
