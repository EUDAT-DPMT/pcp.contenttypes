"""Definition of the ServiceComponentOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponentOffer
from pcp.contenttypes.config import PROJECTNAME

ServiceComponentOfferSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ServiceComponentOfferSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponentOffer(folder.ATFolder):
    """Provider offers service components"""
    implements(IServiceComponentOffer)

    meta_type = "ServiceComponentOffer"
    schema = ServiceComponentOfferSchema


atapi.registerType(ServiceComponentOffer, PROJECTNAME)
