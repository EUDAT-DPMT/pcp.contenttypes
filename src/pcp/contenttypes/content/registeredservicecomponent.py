"""Definition of the RegisteredServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.config import PROJECTNAME

RegisteredServiceComponentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredServiceComponentSchema, moveDiscussion=False)


class RegisteredServiceComponent(base.ATCTContent):
    """A CDI admin registers a new service component"""
    implements(IRegisteredServiceComponent)

    meta_type = "RegisteredServiceComponent"
    schema = RegisteredServiceComponentSchema


atapi.registerType(RegisteredServiceComponent, PROJECTNAME)
