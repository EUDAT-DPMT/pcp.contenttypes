"""Definition of the ServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IServiceComponent
from pcp.contenttypes.config import PROJECTNAME

ServiceComponentSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ServiceComponentSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceComponent(folder.ATFolder):
    """Component of an EUDAT service"""
    implements(IServiceComponent)

    meta_type = "ServiceComponent"
    schema = ServiceComponentSchema


atapi.registerType(ServiceComponent, PROJECTNAME)
