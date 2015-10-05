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
                         widget=atapi.ReferenceWidget(label="Preferred providers",
                                                      ),
                         ),
    ateapi.RecordsField('compute_resources',
                        required=0,
                        minimalSize=2,
                        subfields = ('cpus', 'memory', 'disk', 
                                     'virtualization', 'software'),
                        subfield_types = {'virtualization': 'selection'},
                        subfield_labels ={'cpus':'CPUs',
                                          'virtualization':'virtualization OK?',
                                          'software':'requires OS/software',
                                          },
                        subfield_vocabularies = {'virtualization': 'yesno'},
                        widget=ateapi.RecordsWidget(label='Compute resources'),
                        ),
    ateapi.RecordsField('storage_resources',
                        required=0,
                        minimalSize=2,
                        subfields = ('size', 'type'),
                        subfield_vocabularies = {'type':'storageTypes'},
                        widget=ateapi.RecordsWidget(label='Storage resources'),
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

    def yesno(self, instance):
        """Seems like RecordsFields do not support checkboxes"""
        return atapi.DisplayList([['', 'Select'], ['yes', 'yes'], ['no', 'no']])


atapi.registerType(ResourceRequest, PROJECTNAME)
