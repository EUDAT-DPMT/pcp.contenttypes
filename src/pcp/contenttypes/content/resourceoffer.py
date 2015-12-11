"""Definition of the ResourceOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IResourceOffer
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import CommonUtilities

ResourceOfferSchema = schemata.ATContentTypeSchema.copy() + ResourceFields.copy()


schemata.finalizeATCTSchema(ResourceOfferSchema, moveDiscussion=False)


class ResourceOffer(base.ATCTContent, CommonUtilities):
    """Provider offers compute or storage resources"""
    implements(IResourceOffer)

    meta_type = "ResourceOffer"
    schema = ResourceOfferSchema


atapi.registerType(ResourceOffer, PROJECTNAME)
