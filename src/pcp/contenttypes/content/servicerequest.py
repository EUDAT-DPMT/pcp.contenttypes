"""Definition of the ServiceRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import RequestFields
from pcp.contenttypes.content.common import RequestUtilities

ServiceRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('service',
                         relationship='service',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Service',
                                                       description='The service '
                                                       'being requested',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       allow_search=1,
                                                       ),
                         ),
    atapi.ReferenceField('service_hours',
                         relationship='service_hours',
                         allowed_types=('Document',),
                         widget=ReferenceBrowserWidget(label='Service hours',
                                                       allow_search=1,
                                                       base_query={
                                                           'Subject': ["Support hours"]},
                                                       show_results_without_query=1,
                                                       ),
                         ),
)) + RequestFields.copy() + atapi.Schema((
    ateapi.CommentField('resource_comment',
                        comment="If applicable and already known how much resources shall be provisioned "
                        "through this service then this should be specified here. Otherwise this "
                        "can be left empty (or added later).",
                        ),
)) + ResourceFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceRequestSchema, moveDiscussion=False)


class ServiceRequest(folder.ATFolder, CommonUtilities, RequestUtilities):
    """A project requests a service"""
    implements(IServiceRequest)

    meta_type = "ServiceRequest"
    schema = ServiceRequestSchema


atapi.registerType(ServiceRequest, PROJECTNAME)
