"""Definition of the RegisteredComputeResource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IRegisteredComputeResource
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities
from pcp.contenttypes.content.common import ResourceContextFields


RegisteredComputeResourceSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField('hostname',
                      searchable=True,
                  ), 

    atapi.StringField('ip',
                      searchable=True,
                  ), 

    atapi.StringField('cpus',
                      searchable=True,
                  ), 

    atapi.StringField('memory',
                      searchable=True,
                  ), 

    atapi.StringField('localdisk',
                      searchable=True,
                  ), 

    atapi.StringField('virtualization',
                      searchable=True,
                  ), 

    atapi.StringField('os',
                      searchable=True,
                  ), 

    atapi.StringField('software',
                      searchable=True,
                  ), 

)) + ResourceContextFields.copy() + CommonFields.copy()


schemata.finalizeATCTSchema(RegisteredComputeResourceSchema, moveDiscussion=False)


class RegisteredComputeResource(base.ATCTContent, CommonUtilities):
    """A provisioned physical or virtual server"""
    implements(IRegisteredComputeResource)

    meta_type = "RegisteredComputeResource"
    schema = RegisteredComputeResourceSchema


atapi.registerType(RegisteredComputeResource, PROJECTNAME)
