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

    ReferenceField('service',
                   relationship='forService',
                   multiValued=False,
                   languageIndependent=True,
                   write_permission=ModifyPortalContent,
                   widget=ReferenceBrowserWidget(
                       allow_search=True,
                       allow_browse=True,
                       show_indexes=False,
                       show_path=1,
                       force_close_on_insert=True,
                       startup_directory='/services',
                       base_query={'portal_type': 'Service'},
                       label=_(u'label_service',
                               default=u'Related service'),
                       description='',
                       visible={'edit': 'visible', 'view': 'invisible'}
                   )
                   ),

    ReferenceField('actionItems',
                   relationship='hasActionItem',
                   multiValued=True,
                   isMetadata=True,
                   languageIndependent=False,
                   index='KeywordIndex',
                   write_permission=ModifyPortalContent,
                   widget=ReferenceBrowserWidget(
                       allow_search=True,
                       allow_browse=True,
                       show_indexes=False,
                       allow_sorting=1,
                       show_path=1,
                       force_close_on_insert=True,
                       base_query={'portal_type': 'ActionItem'},
                       label=_(u'label_action_items', default=u'Action Items'),
                       description='',
                       visible={'edit': 'visible', 'view': 'invisible'}
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

        tracker_id = 'tracker-actions'

        target_folder = plone.api.portal.get().restrictedTraverse(target_path, None)
        if target_folder is None:
            raise ValueError(
                'No target object found for {0}'.format(target_path))

        if not tracker_id in target_folder.objectIds():
            tracker = plone.api.content.create(
                container=target_folder,
                type='PoiTracker',
                id=tracker_id,
                title='ActionTracker')
            tracker.setAvailableAreas([])
        else:
            tracker = target_folder[tracker_id]

        available_areas = list(tracker.getAvailableAreas())
        available_areas.append({
            'id': self.getId(),
            'title': self.Title(),
            'description': self.Description()
            })
        tracker.setAvailableAreas(available_areas)

        issues_types = [
           {'id': 'todo', 'title': 'To Do', 'description': 'To Do'},
           {'id': 'bug', 'title': 'Bug', 'description': 'Bug'},
           {'id': 'discussion', 'title': 'Discussion', 'description': 'Discussion'},
        ]
        tracker.setAvailableIssueTypes(issues_types)

        tracker.setAvailableSeverities(['Low', 'Medium', 'High'])

        for num, action in enumerate(self.getActionItems()):
            id_ = '{:03d}-{}'.format(num+1, action.getId())
            if id_ in tracker.objectIds():
                continue
            tracker.invokeFactory('PoiIssue', id_)
            issue = tracker[id_]
            issue.setTitle(action.Title() or id_)
            issue.setArea(self.getId())
            issue.setIssueType('bug')
            issue.setDetails('Foo')
            issue.reindexObject()
            plone.api.content.transition(obj=issue, transition='post')

        tracker.reindexObject()
        return self.REQUEST.RESPONSE.redirect(tracker.absolute_url())

atapi.registerType(ActionList, PROJECTNAME)
