"""Definition of the ServiceOffer content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceOffer
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import ConditionsFields
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

ServiceOfferSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.ReferenceField('service',
                         relationship='service_offered',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Service offered',
                                                       description='Reference to the catalog entry of the service being offered.',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       ),
                         ),
    atapi.ReferenceField('slas',
                         relationship='slas_offered',
                         allowed_types=('Document',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='SLAs offered',
                                                       description='Potential Service Level Agreements under which the service is being offered.',
                                                       allow_browse=1,
                                                       startup_directory='/services/hours',
                                                       ),

                         ),
    atapi.ReferenceField('contact',
                         relationship='contact_for',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Contact',
                                                       description='Contact responsible for this service offer.',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
)) + ConditionsFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceOfferSchema, moveDiscussion=False)


class ServiceOffer(base.ATCTContent, CommonUtilities):
    """Providers signal their service offerings"""
    implements(IServiceOffer)

    meta_type = "ServiceOffer"
    schema = ServiceOfferSchema


atapi.registerType(ServiceOffer, PROJECTNAME)
