"""Definition of the Community content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import ICommunity
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


CommunitySchema = folder.ATFolderSchema.copy() + atapi.Schema((
    
    ateapi.UrlField('url'),
    ateapi.AddressField('address'),
    atapi.ReferenceField('representative',
                         relationship='representative',
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Representative',
                                                      ),
                        ),
    atapi.ReferenceField('admins',
                         relationship='community_admins',
                         multiValued=True,
                         allowed_types=('Person',),
                         widget=atapi.ReferenceWidget(label='Administrators',
                                                      ),
                        ),
    BackReferenceField('affiliated',
                       relationship='affiliated',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),                       
                       ),    
    BackReferenceField('projects_involved',
                       relationship='done_for',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Projects involved',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    CommunitySchema,
    folderish=True,
    moveDiscussion=False
)


class Community(folder.ATFolder, CommonUtilities):
    """A community served by a project on this site."""
    implements(ICommunity)

    meta_type = "Community"
    schema = CommunitySchema


atapi.registerType(Community, PROJECTNAME)
