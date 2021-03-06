"""Definition of the ServiceComponentImplementation content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponentImplementation
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceComponentImplementationSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    BackReferenceField('offered_by',
                       relationship='service_component_implementations_offered',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Offered by',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),
    BackReferenceField('requested_by',
                       relationship='requested_component_implementations',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Requested by',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),

)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceComponentImplementationSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponentImplementation(folder.ATFolder, CommonUtilities):
    """Specific implementation of a service component"""
    implements(IServiceComponentImplementation)

    meta_type = "ServiceComponentImplementation"
    schema = ServiceComponentImplementationSchema


atapi.registerType(ServiceComponentImplementation, PROJECTNAME)
