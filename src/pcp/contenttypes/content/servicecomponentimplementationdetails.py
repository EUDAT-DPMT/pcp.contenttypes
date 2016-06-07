"""Definition of the ServiceComponentImplementationDetails content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponentImplementationDetails
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceComponentImplementationDetailsSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

)) + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceComponentImplementationDetailsSchema, moveDiscussion=False)


class ServiceComponentImplementationDetails(base.ATCTContent, CommonUtilities):
    """Details of a specific implementation of a service component"""
    implements(IServiceComponentImplementationDetails)

    meta_type = "ServiceComponentImplementationDetails"
    schema = ServiceComponentImplementationDetailsSchema


atapi.registerType(ServiceComponentImplementationDetails, PROJECTNAME)
