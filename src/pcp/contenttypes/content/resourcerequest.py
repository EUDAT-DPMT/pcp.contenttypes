"""Definition of the ResourceRequest content type
"""

from zope.interface import implements

from DateTime.DateTime import DateTime
from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from pcp.contenttypes.interfaces import IResourceRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import CommonUtilities

END_OF_EUDAT2020 = "2018-02-28"

ResourceRequestSchema = schemata.ATContentTypeSchema.copy()  + ResourceFields.copy() \
                        + atapi.Schema((
    atapi.DateTimeField('startDate',
                        widget=atapi.CalendarWidget(label='Start date',
                                                    show_hm=False),
                        ),
    atapi.DateTimeField('endDate',
                        default=DateTime(END_OF_EUDAT2020),
                        widget=atapi.CalendarWidget(label='End date',
                                                    show_hm=False),
                        ),
    atapi.StringField('ticketid'),
    atapi.ReferenceField('preferred_providers',
                         relationship='preferred_providers',
                         multiValued=True,
                         allowed_types=('Provider',),
                         widget=atapi.ReferenceWidget(label="Preferred provider(s)",
                                                      ),
                         ),

)) + ResourceFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(ResourceRequestSchema, moveDiscussion=False)


class ResourceRequest(base.ATCTContent, CommonUtilities):
    """A project requests a storage or compute resource"""
    implements(IResourceRequest)

    meta_type = "ResourceRequest"
    schema = ResourceRequestSchema

    def request_details(self):
        """Helper method used for string interpolation"""
        values = []
        compute = self.getCompute_resources()
        storage = self.getStorage_resources()
        if compute:
            values.append("Compute: %s" % compute)
        if storage:
            values.append("Storage: %s" % storage)
        return "\n".join(values)


atapi.registerType(ResourceRequest, PROJECTNAME)
