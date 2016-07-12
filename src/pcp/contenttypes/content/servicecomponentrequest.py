"""Definition of the ServiceComponentRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceComponentRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

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
    atapi.ReferenceField('service_providers',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='preferred_providers',
                         allowed_types=('Provider',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Preferred service provider(s)',
                                                       description='The provider(s) preferred '\
                                                       'for hosting this service component '\
                                                       '- if any.',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                      ),
                         ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceComponentRequestSchema, moveDiscussion=False)


class ServiceComponentRequest(folder.ATFolder, CommonUtilities):
    """A project requests a specific service component"""
    implements(IServiceComponentRequest)

    meta_type = "ServiceComponentRequest"
    schema = ServiceComponentRequestSchema

atapi.registerType(ServiceComponentRequest, PROJECTNAME)
