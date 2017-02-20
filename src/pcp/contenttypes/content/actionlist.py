"""Definition of the ServiceComponent content type
"""

import plone.api
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
                show_path=1,
                force_close_on_insert = True,
                base_query={'portal_type': 'ActionItem'},
                label = _(u'label_action_items', default=u'Action Items'),
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

    _at_rename_after_creation = True

    def createPOI(self, target_path):
        """ ActionList to Poi """

        target_folder = plone.api.portal.get().restrictedTraverse(target_path, None)
        if target_folder is None:
            raise ValueError('No target object found for {0}'.format(target_path))

        tracker = plone.api.content.create(
                container=target_folder,
                type='PoiTracker',
                id='tracker-actions',
                title='Actions ()'.format(self.getId()))

        for action in self.getActionItems():
            tracker.invokeFactory('PoiIssue', action.getId())
            issue = tracker[action.getId()]
            issue.setTitle(action.Title() or action.getId())
            issue.setArea('functionality')
            issue.setIssueType('bug')
            issue.setDetails('Foo')
            issue.reindexObject()
            plone.api.content.transition(obj=issue, transition='post')

        tracker.reindexObject()
        return self.REQUEST.RESPONSE.redirect(tracker.absolute_url())

atapi.registerType(ActionList, PROJECTNAME)
