"""Definition of the ServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.atapi import BaseContent
from Products.ATContentTypes.content import schemata


# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IActionItem
from pcp.contenttypes.config import PROJECTNAME


ActionItemSchema = BaseContent.schema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(
    ActionItemSchema,
    folderish=False,
    moveDiscussion=False
)


class ActionItem(BaseContent):
    """Component of an EUDAT service"""
    implements(IActionItem)

    meta_type = "ActionItem"
    schema = ActionItemSchema


atapi.registerType(ActionItem, PROJECTNAME)
