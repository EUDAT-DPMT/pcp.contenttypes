"""Definition of the ServiceRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

ServiceRequestSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ReferenceField('service',
                         relationship='service',
                         allowed_types=('Service',),
                         ),
    ateapi.RecordField('size',
                       subfields=('value', 'unit'),
                       ),
    atapi.StringField('storage_type',
                      vocabulary='storageTypes',
                      widget=atapi.SelectionWidget(),
                      ),                  
)) + CommonFields.copy()


schemata.finalizeATCTSchema(ServiceRequestSchema, moveDiscussion=False)


class ServiceRequest(base.ATCTContent, CommonUtilities):
    """A project requests a service"""
    implements(IServiceRequest)

    meta_type = "ServiceRequest"
    schema = ServiceRequestSchema

    def getSize(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['size'].get(self)
        return self.convert(raw)

    def storageTypes(self):
        return ateapi.getDisplayList(self, 'storage_types', add_select=True)

atapi.registerType(ServiceRequest, PROJECTNAME)
