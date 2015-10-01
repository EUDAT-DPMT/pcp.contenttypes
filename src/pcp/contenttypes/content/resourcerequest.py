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
from pcp.contenttypes.content.common import CommonUtilities


ResourceRequestSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.DateTimeField('startDate',
                        widget=atapi.CalendarWidget(show_hm=False),
                        ),
    atapi.DateTimeField('endDate',
                        widget=atapi.CalendarWidget(show_hm=False),
                        ),
    atapi.StringField('ticketid'),
    atapi.ReferenceField('preferred_providers',
                         relationship='preferred_providers',
                         multiValued=True,
                         allowed_types=('Provider',),
                         widget=atapi.ReferenceWidget(label="Preferred provider",
                                                      ),
                         ),
    ateapi.RecordsField('compute_resources',
                        required=0,
                        minimalSize=3,
                        subfields = ('cpus', 'memory', 'disk', 
                                     'virtualization', 'software'),
                        subfield_labels ={'cpus':'CPUs',
                                          'virtualization':'virtualization OK?',
                                          'software':'requires OS/software',
                                          },
                        ),
    ateapi.RecordsField('storage_resources',
                        required=0,
                        minimalSize=3,
                        subfields = ('size', 'type'),
                        subfield_vocabularies = {'type':'storageTypes'},
                        ),

)) + CommonFields.copy()


schemata.finalizeATCTSchema(ResourceRequestSchema, moveDiscussion=False)


class ResourceRequest(base.ATCTContent, CommonUtilities):
    """A project requests a storage or compute resource"""
    implements(IResourceRequest)

    meta_type = "ResourceRequest"
    schema = ResourceRequestSchema

    def storageTypes(self, instance):
        """Look up the controlled vocabulary for the storage types
        from the properties tool"""
        
        return ateapi.getDisplayList(instance, 'storage_types', add_select=True)


atapi.registerType(ResourceRequest, PROJECTNAME)
