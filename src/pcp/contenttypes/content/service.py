"""Definition of the Service content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IService
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ServiceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField('description_internal',
                      read_permission='View internals',
                      write_permission='Modify internals',
                  ),
    ateapi.UrlField('url',
                    searchable=1,
                ),
    atapi.StringField('service_area',
                  ),
    atapi.StringField('service_type',
                  ),
    atapi.StringField('value_to_customer',
                  ),
    atapi.StringField('risks',
                  ),
    atapi.StringField('funders_for_service',
                  ),
    atapi.StringField('request_procedures',
                  ),
    ateapi.UrlField('helpdesk',
                    searchable=1,
                ),
    atapi.ReferenceField('managed_by',
                         relationship='managed_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Managed by',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('service_owner',
                         relationship='owned_by',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Service owner',
                                                       allow_browse=1,
                                                       startup_directory='/contacts',
                                                       ),
                         ),
    atapi.ReferenceField('contact',
                         relationship='contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Contact',
                                                       allow_browse=1,
                                                       startup_directory='/contacts',
                                                       ),
                         ),
    ateapi.UrlField('service_complete_link',
                    read_permission='View internals',
                    write_permission='Modify internals',
                ),
    atapi.StringField('competitors',
                      read_permission='View internals',
                      write_permission='Modify internals',
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
