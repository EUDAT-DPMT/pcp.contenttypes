"""Definition of the Resource content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IResource
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ResourceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('managed_by',
                         relationship='managed_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Managed by',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('hosted_by',
                         relationship='hosted_by',
                         allowed_types=('Provider',),
                         widget=ReferenceBrowserWidget(label='Hosted by',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                       ),
                        ),
    atapi.ReferenceField('used_by',
                         relationship='used_by',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Used by',
                                                       allow_browse=1,
                                                       startup_directory='/services',
                                                       ),
                        ),                     
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ResourceSchema,
    folderish=True,
    moveDiscussion=False
)


class Resource(folder.ATFolder, CommonUtilities):
    """A resource needed to provide a service managed by a project on this site."""
    implements(IResource)

    meta_type = "Resource"
    schema = ResourceSchema


atapi.registerType(Resource, PROJECTNAME)
