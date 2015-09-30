"""Definition of the ResourceOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IResourceOffer
from pcp.contenttypes.config import PROJECTNAME

ResourceOfferSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(ResourceOfferSchema, moveDiscussion=False)


class ResourceOffer(base.ATCTContent):
    """Provider offers compute or storage resources"""
    implements(IResourceOffer)

    meta_type = "ResourceOffer"
    schema = ResourceOfferSchema


atapi.registerType(ResourceOffer, PROJECTNAME)
