"""Definition of the Downtime content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IDowntime
from pcp.contenttypes.config import PROJECTNAME

DowntimeSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(DowntimeSchema, moveDiscussion=False)


class Downtime(base.ATCTContent):
    """Scheduled downtime"""
    implements(IDowntime)

    meta_type = "Downtime"
    schema = DowntimeSchema


atapi.registerType(Downtime, PROJECTNAME)
