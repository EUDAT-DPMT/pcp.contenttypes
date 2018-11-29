"""Definition of the ServiceComponentOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceComponentOffer
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import ConditionsFields
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import OfferUtilities
from pcp.contenttypes.content.common import CommonUtilities

ServiceComponentOfferSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('service_component',
                         relationship='service_component_offered',
                         allowed_types=('ServiceComponent',),
                         widget=ReferenceBrowserWidget(label='Service component offered',
                                                       description='Reference to the catalog entry of the service component being offered.',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       ),
                         ),
    atapi.ReferenceField('implementations',
                         relationship='service_component_implementations_offered',
                         allowed_types=('ServiceComponentImplementation',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Implementations offered',
                                                       description='Reference to the catalog entry of the implementations(s) of the service component being offered.',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       ),
                         ),
)) + ConditionsFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceComponentOfferSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponentOffer(folder.ATFolder, CommonUtilities, OfferUtilities):
    """Provider offers service components"""
    implements(IServiceComponentOffer)

    meta_type = "ServiceComponentOffer"
    schema = ServiceComponentOfferSchema


atapi.registerType(ServiceComponentOffer, PROJECTNAME)
