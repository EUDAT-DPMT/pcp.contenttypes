"""Definition of the Project content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import IProject
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('community',
                         relationship='done_for',
                         allowed_types=('Community',),
                         ),    
    atapi.ReferenceField('community_contact',
                         relationship='community_contact',
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Community contact',
                                                      ),
                         ),
    atapi.ReferenceField('service_provider',
                         relationship='provided_by',
                         allowed_types=('Center',),
                         widget=atapi.ReferenceWidget(label='Service provider',
                                                      ),
                         ),
    atapi.ReferenceField('services_used',
                         relationship='using',
                         allowed_types=('Service',),
                         widget=atapi.ReferenceWidget(label='Services used',
                                                      ),
                         ),
    ateapi.RecordField('resources',
                       subfields=('allocated (TB)', 'used (TB)', '# of objects'),
                       ),
    atapi.ReferenceField('project_enabler',
                         relationship='enabled_by',
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Enabled by',
                                                      ),
                         ),
    atapi.DateTimeField('start_date',
                        widget=atapi.CalendarWidget(label='Start date',
                                                    show_hm=False,
                                                    ),
                        ),
    ateapi.UrlField('call_for_collaboration',
                    widget=ateapi.UrlWidget(label='Call for collaboration',
                                            description='URL to the call that '\
                                            'triggered this project',
                                            ),
                    ),
    ateapi.UrlField('uptake_plan',
                    widget=ateapi.UrlWidget(label='Uptake plan',
                                            description='URL to the projects '\
                                            'uptake plan (if not on this site). '\
                                            'Often to be found on the '\
                                            'confluence site.',
                                            ),
                    ),
    atapi.StringField('repository'),
    atapi.StringField('topics'),
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


atapi.registerType(Project, PROJECTNAME)
