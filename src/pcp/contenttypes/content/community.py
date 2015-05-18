"""Definition of the Community content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import ICommunity
from pcp.contenttypes.config import PROJECTNAME

CommunitySchema = folder.ATFolderSchema.copy() + atapi.Schema((
    
    ateapi.UrlField('url'),
    ateapi.AddressField('address'),
    BackReferenceField('affiliated',
                       relationship='affiliated',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),                       
                       ),    
))


schemata.finalizeATCTSchema(
    CommunitySchema,
    folderish=True,
    moveDiscussion=False
)


class Community(folder.ATFolder):
    """A community served by a project on this site."""
    implements(ICommunity)

    meta_type = "Community"
    schema = CommunitySchema


atapi.registerType(Community, PROJECTNAME)
