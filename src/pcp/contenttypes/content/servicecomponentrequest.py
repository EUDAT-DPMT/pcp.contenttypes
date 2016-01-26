"""Definition of the ServiceComponentRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IServiceComponentRequest
from pcp.contenttypes.config import PROJECTNAME

ServiceComponentRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(ServiceComponentRequestSchema, moveDiscussion=False)


class ServiceComponentRequest(folder.ATFolder):
    """A project requests a specific service component"""
    implements(IServiceComponentRequest)

    meta_type = "ServiceComponentRequest"
    schema = ServiceComponentRequestSchema

    atapi.ReferenceField('service_providers',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='preferred_providers',
                         allowed_types=('Provider',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Preferred service provider(s)',
                                                       description='The provider(s) preferred for hosting this service component.',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                      ),
                         ),


atapi.registerType(ServiceComponentRequest, PROJECTNAME)
