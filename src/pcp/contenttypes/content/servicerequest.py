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

ServiceRequestSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ReferenceField('service',
                         relationship='service',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Service',
                                                       allow_search=1,
                                                       allow_browse=0,
                                                       base_query={'portal_type':'Service'},
                                                       show_results_without_query=1,
                                                       only_for_review_states=['published'],
                                                       ),
                         ),
    ateapi.RecordField('size',
                       subfields=('value', 'unit', 'type'),
                       subfield_vocabularies = {'unit': 'informationUnits',
                                                'type': 'storageTypes',
                                                },
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
#    atapi.StringField('storage_type',
#                      vocabulary='storageTypes',
#                      widget=atapi.SelectionWidget(),
#                      ),                  
)) + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceRequestSchema, moveDiscussion=False)


class ServiceRequest(folder.ATFolder, CommonUtilities):
    """A project requests a service"""
    implements(IServiceRequest)

    meta_type = "ServiceRequest"
    schema = ServiceRequestSchema

    def getSize(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['size'].get(self)
        return self.convert(raw)

    def storageTypes(self, instance=None):
        if instance is None:
            return ateapi.getDisplayList(self, 'storage_types', add_select=True)
        return ateapi.getDisplayList(instance, 'storage_types', add_select=True)

atapi.registerType(ServiceRequest, PROJECTNAME)
