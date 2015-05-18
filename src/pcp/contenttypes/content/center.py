"""Definition of the Center content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import ICenter
from pcp.contenttypes.config import PROJECTNAME

CenterSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url'),
    ateapi.AddressField('address'),
))


schemata.finalizeATCTSchema(
    CenterSchema,
    folderish=True,
    moveDiscussion=False
)


class Center(folder.ATFolder):
    """A center providing services managed by projects on this site."""
    implements(ICenter)

    meta_type = "Center"
    schema = CenterSchema


atapi.registerType(Center, PROJECTNAME)
