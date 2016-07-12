"""Definition of the ResourceRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IResourceRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import CommonUtilities


ResourceRequestSchema = schemata.ATContentTypeSchema.copy()  + ResourceFields.copy() \
                        + atapi.Schema((
    atapi.DateTimeField('startDate',
                        widget=atapi.CalendarWidget(label='Start date',
                                                    show_hm=False),
                        ),
    atapi.DateTimeField('endDate',
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



atapi.registerType(ResourceRequest, PROJECTNAME)
