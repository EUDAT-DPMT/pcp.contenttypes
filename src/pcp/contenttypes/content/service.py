"""Definition of the Service content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import IService
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url'),
    atapi.ReferenceField('managed_by',
                         relationship='managed_by',
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Managed by',
                                                      ),
                         ),
    BackReferenceField('resources_used',
                       relationship='used_by',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Resources used',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('used_by_project',
                       relationship='using',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Used by projects',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceSchema,
    folderish=True,
    moveDiscussion=False
)


class Service(folder.ATFolder, CommonUtilities):
    """A service managed by this site."""
    implements(IService)

    meta_type = "Service"
    schema = ServiceSchema


atapi.registerType(Service, PROJECTNAME)
