"""Definition of the ServiceComponent content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponent
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceComponentSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    BackReferenceField('offered_by',
                       relationship='service_component_offered',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Offered by',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),

    BackReferenceField('requested_by',
                       relationship='requested_component',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Requested by',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),

)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceComponentSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponent(folder.ATFolder, CommonUtilities):
    """Component of an EUDAT service"""
    implements(IServiceComponent)

    meta_type = "ServiceComponent"
    schema = ServiceComponentSchema


atapi.registerType(ServiceComponent, PROJECTNAME)
