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
                                                  visible={'view': 'invisible', 'edit': 'visible'} ,
                                                  ),
                       ),
    atapi.ComputedField('usage',
                        expression='here.renderMemoryValue(here.getUsedMemory() and here.getUsedMemory()["core"])',
                        widget=atapi.ComputedWidget(label='Current usage'),
                    ),
    atapi.ComputedField('number',
                        expression='here.getNumberOfRegisteredObjects()',
                        widget=atapi.ComputedWidget(label='Registered objects'),
                    ),
    atapi.ComputedField('allocated',
                        expression='here.renderMemoryValue(here.getAllocatedMemory())',
                        widget=atapi.ComputedWidget(label='Allocated storage'),
                    ),
    atapi.ComputedField('storage_class',
                        expression='here.getStorageClass()',
                        widget=atapi.ComputedWidget(label='Storage class'),
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

    def getStorageClass(self):
        size = self.schema['size'].get(self)
        return size.get('storage class', '')

    def getCachedRecords(self):
        return getattr(self, 'cached_records', None)

    def getUsedMemory(self):
        return getattr(self, 'cached_newest_record', None)

    def getAllocatedMemory(self):
        raw = self.schema['size'].get(self)
        if 'value' in raw and 'unit' in raw:
            # unit should be enforced by field's vocabulary
            try:
                float(raw['value'])
            except ValueError:
                return None
            return raw
        else:
            return None

    def getResourceUsage(self):
        used = self.getUsedMemory()
        size = self.getAllocatedMemory()

        if used:
            meta = used['meta']
            submission_time = meta['submission_time']
        else:
            submission_time = '??'

        return '%s (%s UTC)' % (self.renderResourceUsage(used and used['core'], size), 
                                submission_time)

    def getNumberOfRegisteredObjects(self, as_int=False):
        used = self.getUsedMemory()
        number = None
        if used:
            number = used['meta'].get('number', None)
        if as_int:
            if number in [None, '']:
                return 0
            else:
                return int(number)
        return number

    def getScopeValues(self, asString = 0):
        """Return the human readable values of the scope keys"""
        project = self.getProject()
        if project is None:
            if asString:
                return ''
            else:
                return ('',)
        scopes = []
        scopes.extend(project.getScopeValues())
        s = set(scopes)
        if  asString:
            return ", ".join(s)
        return s # tuple(s)


atapi.registerType(RegisteredStorageResource, PROJECTNAME)
