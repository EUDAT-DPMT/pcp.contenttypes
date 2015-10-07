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
                         relationship='done_for',
                         allowed_types=('Community',),
                         widget=ReferenceBrowserWidget(label='Community',
                                                       allow_browse=1,
                                                       startup_directory='/communities',
                                                       ),
                         ),    
    atapi.ReferenceField('community_contact',
                         relationship='community_contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Community contact',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('service_provider',
                         relationship='provided_by',
                         allowed_types=('Provider',),
                         widget=ReferenceBrowserWidget(label='Service provider',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                      ),
                         ),
    atapi.ReferenceField('services_used',
                         relationship='using',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Services used',
                                                       allow_browse=1,
                                                       startup_directory='/services',
                                                      ),
                         ),
#    ateapi.RecordField('resources',
#                       subfields=('allocated (TB)', 'used (TB)', '# of objects'),
#                       ),
    ateapi.RecordField('allocated',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       ),
    ateapi.RecordField('used',
                       subfields=('value', 'unit'),
                       subfield_vocabularies={'unit': 'informationUnits'},
                       ),
    atapi.ReferenceField('project_enabler',
                         relationship='enabled_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Enabled by',
                                                       allow_browse=1,
                                                       startup_directory='/people',
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

    def getAllocated(self):
        """Specialized accessor that can handle unit conversions."""

        raw = self.schema['allocated'].get(self)
        return self.convert(raw)

    def getUsed(self):
        """Specialized accessor supporting unit conversion"""
        raw = self.schema['used'].get(self)
        return self.convert(raw)
    

atapi.registerType(Project, PROJECTNAME)

