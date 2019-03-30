"""Definition of the Project content type
"""

from pcp.contenttypes.interfaces import IRegisteredComputeResource
from pcp.contenttypes.interfaces import IRegisteredStorageResource
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary ##neu

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IProject
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('website'),
    atapi.ReferenceField('community',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='done_for',
                         allowed_types=('Community',),
                         widget=ReferenceBrowserWidget(label='Customer',
                                                       description='Main customer '
                                                       'involved in this project',
                                                       allow_browse=1,
                                                       startup_directory='/customers',
                                                       ),
                         ),
    atapi.ReferenceField('community_contact',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='community_contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Customer contact',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('registered_services_used',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='using',
                         multiValued=1,
                         allowed_types=('RegisteredService',),
                         widget=ReferenceBrowserWidget(label='Registered services used',
                                                       description="Select all registered services the project requires",
                                                       allow_browse=1,
                                                       startup_directory='/operations',
                                                       condition='python:here.stateIn(["enabling","pre_production","production","terminated"])'),

                         ),
    atapi.ComputedField('allocated_new',
                        expression='here.renderMemoryValue(here.convert(here.getStorageResourcesSizeSummary(here.getResources())))',
                        widget=atapi.ComputedWidget(label='Allocated'),
                       ),
    atapi.ComputedField('used_new',
                        expression='here.renderMemoryValue(here.convert(here.getStorageResourcesUsedSummary(here.getResources())))',
                        widget=atapi.ComputedWidget(label='Used'),
                        ),
    atapi.ReferenceField('general_provider',
                         relationship='general_provider',
                         allowed_types=('Provider',),
                         widget=ReferenceBrowserWidget(label='General provider',
                                                       description='General provider for this project (chose EUDAT Ltd if in doubt)',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                       ),
                         ),
    atapi.ReferenceField('project_enabler',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='enabled_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Project enabled by',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       condition="python:here.stateNotIn(['considered'])",
                                                       ),
                         ),
    atapi.DateTimeField('start_date',
                        widget=atapi.CalendarWidget(label='Start date',
                                                    show_hm=False,
                                                    condition="python:here.stateNotIn(['considered'])",
                                                    ),
                        ),
    atapi.DateTimeField('end_date',
                        widget=atapi.CalendarWidget(label='End date',
                                                    show_hm=False,
                                                    condition="python:here.stateNotIn(['considered'])",
                                                    ),
                        ),
    ateapi.UrlField('call_for_collaboration',
                    widget=ateapi.UrlWidget(label='Call for collaboration',
                                            description='URL to the call that '
                                            'triggered this project',
                                            ),
                    ),
    ateapi.UrlField('uptake_plan',
                    read_permission='View internals',
                    write_permission='Modify internals',
                    widget=ateapi.UrlWidget(label='Uptake plan',
                                            description='URL to the project '
                                            'uptake plan (if not available on this site). '
                                            'Otherwise, often found on the '
                                            'confluence site.',
                                            ),
                    ),
    atapi.StringField('repository',
                      widget=atapi.StringWidget(description="If the data to be "
                                                "dealt with here are in a web-accessible "
                                                "repository already you should specify "
                                                "its URL here.",),
                      ),
    atapi.StringField('topics',
                      widget=atapi.StringWidget(description='Please mention the '
                                                'scientific field(s) the data '
                                                'originate from.'),
                      ),
    atapi.LinesField('scopes',
                      required=1,
                      vocabulary=NamedVocabulary('scope_vocabulary'),
                      widget=atapi.MultiSelectionWidget(description='Tick all that apply. '
                                                        'If in doubt, select "EUDAT".',
                                                        format='checkbox',
                                                    ),
                      ),
    BackReferenceField('resources',
                       relationship='project',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Resources',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),
    atapi.ComputedField('resource_usage',
                  expression='here.listResourceUsage(here.getResources())',
                  widget=atapi.ComputedWidget(label='Resource Usage'),
                  ),
    atapi.ComputedField('registered_objects',
                  expression='here.registeredObjectsTotal()',
                  widget=atapi.ComputedWidget(label='Registered objects'),
                  ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)


class Project(folder.ATFolder, CommonUtilities):
    """A project managed by this site."""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema

    def getAllocated(self):
        """Specialized accessor that can handle unit conversions."""
        raw = self.schema['allocated'].get(self)
        return self.convert(raw)

    def getUsed(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['used'].get(self)
        return self.convert(raw)



atapi.registerType(Project, PROJECTNAME)
