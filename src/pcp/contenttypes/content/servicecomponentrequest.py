"""Definition of the ServiceComponentRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceComponentRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import RequestFields
from pcp.contenttypes.content.common import RequestUtilities


ServiceComponentRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('service_component',
                         relationship='requested_component',
                         allowed_types=('ServiceComponent',),
                         multiValued=False,
                         widget=ReferenceBrowserWidget(label='Service component',
                                                       description='The service component '\
                                                       'being requested',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                      ),
                         ),
    atapi.ReferenceField('implementations',
                         relationship='requested_component_implementations',
                         allowed_types=('ServiceComponentImplementation',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Implementation',
                                                       description='If only certain '\
                                                       'implemenations are acceptable, this '\
                                                       'can be specified here. Leave empty '\
                                                       'if any implementation is fine.',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                      ),
                         ),
    atapi.ReferenceField('service_hours',
                         relationship='service_hours',
                         allowed_types=('Document',),
                         widget=ReferenceBrowserWidget(label='Service hours',
                                                       allow_search=1,
                                                       base_query={'Subject':["Support hours"]},
                                                       show_results_without_query=1,
                                                       ),
                         ),
)) + RequestFields.copy() + atapi.Schema((
    ateapi.CommentField('resource_comment',
                        comment="If applicable and already known how much resources shall be provisioned "\
                        "through this service then this should be specified here. Otherwise this "\
                        "can be left empty (or added later).",
                    ),
)) + ResourceFields.copy() + CommonFields.copy()



schemata.finalizeATCTSchema(ServiceComponentRequestSchema, moveDiscussion=False)


class ServiceComponentRequest(folder.ATFolder, CommonUtilities, RequestUtilities):
    """A project requests a specific service component"""
    implements(IServiceComponentRequest)

    meta_type = "ServiceComponentRequest"
    schema = ServiceComponentRequestSchema

atapi.registerType(ServiceComponentRequest, PROJECTNAME)
