"""Definition of the AccountingRecord content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IAccountingRecord
from pcp.contenttypes.config import PROJECTNAME

AccountingRecordSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(AccountingRecordSchema, moveDiscussion=False)


class AccountingRecord(base.ATCTContent):
    """Account storage, CPU cycles or other resource usage"""
    implements(IAccountingRecord)

    meta_type = "AccountingRecord"
    schema = AccountingRecordSchema


atapi.registerType(AccountingRecord, PROJECTNAME)
