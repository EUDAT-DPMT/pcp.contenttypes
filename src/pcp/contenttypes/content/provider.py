"""Definition of the Provider content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProviderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url'),
    ateapi.AddressField('address'),
    atapi.ReferenceField('contact',
                         relationship='contact',
                         allowed_types=('Person',),
                         ),
    atapi.ReferenceField('admins',
                         relationship='admin_of',
                         multiValued=True,
                         allowed_types=('Person',),
                         ),
    atapi.LinesField('supported_os',
                     multiValued=True,
                     vocabulary='getOSVocab',
                     widget=atapi.MultiSelectionWidget(),
                     ),
    atapi.StringField('committed_cores', schemata='resources'),
    atapi.StringField('committed_disk', schemata='resources'),
    atapi.StringField('committed_tape', schemata='resources'),
    atapi.StringField('used_disk', schemata='resources'),
    atapi.StringField('used_tape', schemata='resources'),
    atapi.ReferenceField('communities_primary',
                         relationship='primary_provider_for',
                         multiValued=True,
                         allowed_types=('Community',),
                         ),
    atapi.ReferenceField('communities_secondary',
                         relationship='secondary_provider_for',
                         multiValued=True,
                         allowed_types=('Community',),
                         ),        
    BackReferenceField('affiliated',
                       relationship='affiliated',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('hosts',
                       relationship='hosted_by',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('projects_invloved',
                       relationship='provided_by',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Projects involved',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    ateapi.UrlField('getAccount',
                    widget=ateapi.UrlWidget(label='Account',
                                            description='URL to instructions on how to get an account',
                                            ),
                    ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ProviderSchema,
    folderish=True,
    moveDiscussion=False
)


class Provider(folder.ATFolder, CommonUtilities):
    """Compute or data service provider"""
    implements(IProvider)

    meta_type = "Provider"
    schema = ProviderSchema

    def getOSVocab(self):
        """provides the vocabulary for the 'supported_os' field"""

        return ateapi.getDisplayList(self, 'operating_systems', add_select=False)

atapi.registerType(Provider, PROJECTNAME)
