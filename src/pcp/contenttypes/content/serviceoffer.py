"""Definition of the ServiceOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceOffer
from pcp.contenttypes.config import PROJECTNAME

ServiceOfferSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(ServiceOfferSchema, moveDiscussion=False)


class ServiceOffer(base.ATCTContent):
    """Providers signal their service offerings"""
    implements(IServiceOffer)

    meta_type = "ServiceOffer"
    schema = ServiceOfferSchema


atapi.registerType(ServiceOffer, PROJECTNAME)
