"""Definition of the RegisteredStorageResource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredStorageResource
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities
from pcp.contenttypes.content.common import ResourceContextFields
from pcp.contenttypes.content.accountable import Accountable


RegisteredStorageResourceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    ateapi.RecordField('size',
                       subfields=('value', 'unit', 'storage class'),
                       subfield_sizes={'value': 10,
                                       'storage class': 60,
                                       },
                       subfield_vocabularies={'unit': 'informationUnits',
                                              'storage class': 'storageTypes'},
                       widget=ateapi.RecordWidget(label='Size',
                                                  description='Maximal size and type of this '
                                                  'storage resource',
                                                  ),
                       ),
    atapi.IntegerField('max_objects',
                       widget=atapi.IntegerWidget(label='Max. Objects',
                                                  description='Allocated (maximum) number of objects',
                                                  ),
                       ),
    atapi.FloatField('cost_factor'),
    atapi.DateTimeField('preserve_until',
                        widget=atapi.CalendarWidget(label='Preserve until',
                                                    description='Until when does this resource need '
                                                    'to be allocated?',
                                                    show_hm=False),
                        ),
)) + ResourceContextFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(
    RegisteredStorageResourceSchema, moveDiscussion=False)


class RegisteredStorageResource(base.ATCTContent, CommonUtilities, Accountable):
    """A provisioned storage space of a certain type"""
    implements(IRegisteredStorageResource)

    meta_type = "RegisteredStorageResource"
    schema = RegisteredStorageResourceSchema


atapi.registerType(RegisteredStorageResource, PROJECTNAME)
