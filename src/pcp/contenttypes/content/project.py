"""Definition of the Project content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

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
                                                       description='Main customer '\
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
#TODO: do we need this field at all?
    atapi.ReferenceField('services_used',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='using',
                         multiValued=1,
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Services used',
                                                       description="Select all services the project requires",
                                                       allow_browse=1,
                                                       startup_directory='/services',
                                                       condition='python:here.stateIn(["enabling","pre_production","production","terminated"])'),

                                                      ),
#    ateapi.RecordField('resources',
#                       subfields=('allocated (TB)', 'used (TB)', '# of objects'),
#                       ),
    ateapi.RecordField('allocated',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       widget=ateapi.RecordWidget(condition=
                                                  'python:here.stateIn(["planned","enabling","pre_production","production","terminated"])'),
                       ),
    ateapi.RecordField('used',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       widget=ateapi.RecordWidget(condition=
                                                  'python:here.stateIn(["pre_production","production","terminated"])'),
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
                                            description='URL to the call that '\
                                            'triggered this project',
                                            ),
                    ),
    ateapi.UrlField('uptake_plan',
                    read_permission='View internals',
                    write_permission='Modify internals',
                    widget=ateapi.UrlWidget(label='Uptake plan',
                                            description='URL to the project '\
                                            'uptake plan (if not available on this site). '\
                                            'Otherwise, often found on the '\
                                            'confluence site.',
                                            ),
                    ),
    atapi.StringField('repository',
                      widget=atapi.StringWidget(description="If the data to be "\
                                                "dealt with here are in a web-accessible "\
                                                "repository already you should specify "\
                                                "its URL here.",),
                  ),
    atapi.StringField('topics',
                      widget=atapi.StringWidget(description='Please mention the '\
                                                'scientific field(s) the data '\
                                                'originate from.'),
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

