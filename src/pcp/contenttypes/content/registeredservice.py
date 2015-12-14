"""Definition of the RegisteredService content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.config import PROJECTNAME

RegisteredServiceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.ReferenceField('original_request',
                         relationship='original_request',
                         allowed_types=('ServiceRequest',),
                         widget=ReferenceBrowserWidget(label='Request',
                                                       description='The original request '\
                                                       'that triggered the establishment '\
                                                       'of this service.',
                                                       base_query={'portal_type':'ServiceRequest'},
                                                       allow_search=1,
                                                       allow_browse=0,
                                                       show_results_without_query=1,
                                                       show_review_state=1,
                                                       ),
                         ),
    atapi.ReferenceField('service_components',
                         relationship='service_componemts',
                         multiValued=True,
                         allowed_types=('RegisteredServiceComponent',),
                         widget=ReferenceBrowserWidget(label='Service components',
                                                       description='The service components '\
                                                       'providing the service.',
                                                       base_query={'portal_type':'RegisteredServiceComponent'},
                                                       allow_search=1,
                                                       allow_browse=0,
                                                       show_results_without_query=1,
                                                       ),
                        ),

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredServiceSchema, moveDiscussion=False)


class RegisteredService(base.ATCTContent):
    """A CDI admin registers a new service"""
    implements(IRegisteredService)

    meta_type = "RegisteredService"
    schema = RegisteredServiceSchema


atapi.registerType(RegisteredService, PROJECTNAME)
