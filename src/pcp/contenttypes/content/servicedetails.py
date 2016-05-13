"""Definition of the Service Details content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.ATExtensions import ateapi

from pcp.contenttypes.interfaces import IServiceDetails
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceDetailsSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField('service_status',
                      widget=atapi.StringWidget(label='Status'),
                  ),
    atapi.StringField('version',
                      widget=atapi.StringWidget(label='Version'),
                  ),
    atapi.StringField('use_cases',
                      searchable=1,
                      widget=atapi.StringWidget(label='Use cases'),
                  ),

    ateapi.UrlField('features_current',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Current features'),
                ),
    ateapi.UrlField('features_future',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Future features'),
                ),
    atapi.ReferenceField('dependencies',
                         relationship='depends_on',
                         allowed_types=('Service',),
                         widget=ReferenceBrowserWidget(label='Depends on',
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       ),
                         ),
    ateapi.UrlField('usage_policy_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Usage policy'),
                ),
    ateapi.UrlField('user_documentation_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='User documentation'),
                ),
    ateapi.UrlField('operations_documentation_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Operations documentation'),
                ),
    ateapi.UrlField('monitoring_link',
                    searchable=1,
                    widget=ateapi.UrlWidget(label='Monitoring'),
                ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ServiceDetailsSchema,
    folderish=True,
    moveDiscussion=False
)


class ServiceDetails(folder.ATFolder, CommonUtilities):
    """Detailed information about a service"""
    implements(IServiceDetails)

    meta_type = "ServiceDetails"
    schema = ServiceDetailsSchema


atapi.registerType(ServiceDetails, PROJECTNAME)
