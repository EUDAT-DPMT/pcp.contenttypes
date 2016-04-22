"""Definition of the Community content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

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
                         widget=ReferenceBrowserWidget(label='Representative',
                                                       allow_browse=1,
                                                       description='Main person '\
                                                       'representing the Customer.',
                                                       startup_directory='/people',
                                                       ),
                        ),
    atapi.ReferenceField('admins',
                         relationship='community_admins',
                         multiValued=True,
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Administrators',
                                                       allow_browse=1,
                                                       startup_directory='/people',
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
                                                  description='Projects '\
                                                  'involving this Customer.',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('primary_provider',
                       relationship='primary_provider_for',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Primary provider',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('secondary_provider',
                       relationship='secondary_provider_for',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Secondary provider',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    atapi.StringField('topics',
                      widget=atapi.StringWidget(description='If applicable, please mention the '\
                                                'scientific field(s) this customer '\
                                                'is focussing on.'),
                  ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    CommunitySchema,
    folderish=True,
    moveDiscussion=False
)


class Community(folder.ATFolder, CommonUtilities):
    """A customer served by a project on this site."""
    implements(ICommunity)

    meta_type = "Community"
    schema = CommunitySchema


atapi.registerType(Community, PROJECTNAME)
