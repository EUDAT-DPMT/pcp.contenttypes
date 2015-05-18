"""Definition of the Project content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IProject
from pcp.contenttypes.config import PROJECTNAME

ProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('community',
                         relationship='done_for',
                         allowed_types=('Community',),
                         ),    
    atapi.ReferenceField('community_contact',
                         relationship='community_contact',
                         allowed_types=('Person',),
                         ),
    atapi.ReferenceField('service_provider',
                         relationship='provided_by',
                         allowed_types=('Center',),
                         ),
    atapi.ReferenceField('services_used',
                         relationship='using',
                         allowed_types=('Service',),
                         ),
    ateapi.RecordField('resources',
                       subfields=('allocated (TB)', 'used (TB)', '# of objects'),
                       ),
    atapi.ReferenceField('project_enabler',
                         relationship='enabled_by',
                         allowed_types=('Person',),
                         ),
    atapi.DateTimeField('start_date'),
    ateapi.UrlField('call_for_collaboration'),
    ateapi.UrlField('uptake_plan'),
    atapi.StringField('repository'),
    atapi.StringField('topics'),
))


schemata.finalizeATCTSchema(
    ProjectSchema,
    folderish=True,
    moveDiscussion=False
)


class Project(folder.ATFolder):
    """A project managed by this site."""
    implements(IProject)

    meta_type = "Project"
    schema = ProjectSchema


atapi.registerType(Project, PROJECTNAME)
