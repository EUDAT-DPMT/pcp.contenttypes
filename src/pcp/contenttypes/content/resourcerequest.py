"""Definition of the ResourceRequest content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from pcp.contenttypes.interfaces import IResourceRequest
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import ResourceFields
from pcp.contenttypes.content.common import RequestFields
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities
from pcp.contenttypes.content.common import RequestUtilities


ResourceRequestSchema = schemata.ATContentTypeSchema.copy() \
    + ResourceFields.copy() \
    + RequestFields.copy() \
    + CommonFields.copy()


schemata.finalizeATCTSchema(ResourceRequestSchema, moveDiscussion=False)


class ResourceRequest(base.ATCTContent, CommonUtilities, RequestUtilities):
    """A project requests a storage or compute resource"""
    implements(IResourceRequest)

    meta_type = "ResourceRequest"
    schema = ResourceRequestSchema


atapi.registerType(ResourceRequest, PROJECTNAME)
