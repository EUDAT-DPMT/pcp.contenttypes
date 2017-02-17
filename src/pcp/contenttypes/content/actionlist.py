"""Definition of the ServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.atapi import BaseContent
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IActionList
from pcp.contenttypes.config import PROJECTNAME


ActionListSchema = BaseContent.schema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ActionListSchema,
    folderish=False,
    moveDiscussion=False
)


class ActionList(BaseContent):
    """Component of an EUDAT service"""
    implements(IActionList)

    meta_type = "ActionList"
    schema = ActionListSchema


atapi.registerType(ActionList, PROJECTNAME)
