"""Definition of the Environment content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATExtensions import ateapi

from pcp.contenttypes.interfaces import IEnvironment
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

EnvironmentSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('contact',
                         relationship='contact_for',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(
                             allow_sorting=1,
                             allow_search=1,
                             allow_browse=1,
                             force_close_on_insert=1,
                             startup_directory='/people',
                             use_wildcard_search=True,
                         ),
                         ),
    atapi.TextField('account',
                    widget=atapi.TextAreaWidget(),
                    ),
    ateapi.UrlField('terms_of_use'),
    atapi.BooleanField('rootaccess'),
    atapi.TextField('setup_procedure',
                    widget=atapi.TextAreaWidget(),
                    ),
    atapi.TextField('firewall_policy',
                    widget=atapi.TextAreaWidget(),
                    ),
)) + CommonFields


schemata.finalizeATCTSchema(
    EnvironmentSchema,
    folderish=True,
    moveDiscussion=False
)


class Environment(folder.ATFolder, CommonUtilities):
    """Service Hosting Environment"""
    implements(IEnvironment)

    meta_type = "Environment"
    schema = EnvironmentSchema


atapi.registerType(Environment, PROJECTNAME)
