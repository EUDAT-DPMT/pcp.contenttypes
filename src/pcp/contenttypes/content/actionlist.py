"""Definition of the ServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.Archetypes.atapi import ReferenceField
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.permissions import ModifyPortalContent
from Products.ATContentTypes import ATCTMessageFactory as _

from pcp.contenttypes.interfaces import IActionList
from pcp.contenttypes.config import PROJECTNAME


ActionListSchema = ATContentTypeSchema.copy() + atapi.Schema((

    ReferenceField('actionItems',
            relationship = 'hasActionItem',
            multiValued = True,
            isMetadata = True,
            languageIndependent = False,
            index = 'KeywordIndex',
            write_permission = ModifyPortalContent,
            widget = ReferenceBrowserWidget(
                allow_search = True,
                allow_browse = True,
                show_indexes = False,
                allow_sorting=1,
                force_close_on_insert = True,
                base_query={'portal_type': 'ActionItem'},
                label = _(u'label_action_items', default=u'Action items'),
                description = '',
                visible = {'edit' : 'visible', 'view' : 'invisible' }
                )
            )

))


schemata.finalizeATCTSchema(
    ActionListSchema,
    folderish=False,
    moveDiscussion=False
)


class ActionList(atapi.BaseContent):
    """Component of an EUDAT service"""
    implements(IActionList)

    meta_type = "ActionList"
    schema = ActionListSchema


atapi.registerType(ActionList, PROJECTNAME)
