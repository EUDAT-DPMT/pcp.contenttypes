"""Definition of the RegisteredService content type
"""
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IRegisteredService
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

RegisteredServiceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.ReferenceField('general_provider',
                         relationship='general_provider',
                         allowed_types=('Provider',),
                         widget=ReferenceBrowserWidget(label='General provider',
                                                       description='General provider for this project (chose EUDAT Ltd if in doubt)',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                       ),
                         ),
    atapi.ReferenceField('contact',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='contact_for',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Contact',
                                                       description='The person responsible for this '
                                                       'registered service.',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('managers',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='managers_for',
                         allowed_types=('Person',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Managers(s)',
                                                       description='Other people who can change access '
                                                       'rights and similar critical controls.',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.BooleanField('monitored',
                       widget=atapi.BooleanWidget(label='Should this service be monitored?',
                                                  ),
                       ),
    atapi.ReferenceField('service_components',
                         relationship='service_components',
                         multiValued=True,
                         allowed_types=('RegisteredServiceComponent',),
                         widget=ReferenceBrowserWidget(label='Service components',
                                                       description='The service components '
                                                       'providing the service.',
                                                       base_query={
                                                           'portal_type': 'RegisteredServiceComponent'},
                                                       allow_search=1,
                                                       allow_browse=0,
                                                       show_results_without_query=1,
                                                       ),
                         ),
    atapi.ReferenceField('original_request',
                         relationship='original_request',
                         allowed_types=('ServiceRequest',),
                         widget=ReferenceBrowserWidget(label='Request',
                                                       description='The original request '
                                                       'that triggered the establishment '
                                                       'of this service.',
                                                       base_query={
                                                           'portal_type': 'ServiceRequest'},
                                                       allow_search=1,
                                                       allow_browse=0,
                                                       show_results_without_query=1,
                                                       show_review_state=1,
                                                       ),
                         ),
    atapi.ComputedField('registry_link',
                        expression='here.getCregURL()',
                        widget=atapi.ComputedWidget(label='Central Registry'),
                        ),
    BackReferenceField('used_by_projects',
                       relationship='using',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Used by project',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),
    atapi.ComputedField('scopes',
                        expression='here.getScopeValues(asString = 1)',
                        widget=atapi.ComputedWidget(label='Project Scopes'),
                        ),
    BackReferenceField('resources',
                       relationship='services',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Registered service\'s resources',
                                                  visible={
                                                      'edit': 'invisible'},
                                                  ),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(RegisteredServiceSchema,
                            folderish=True,
                            moveDiscussion=False
)


class RegisteredService(folder.ATFolder, CommonUtilities):
    """A CDI admin registers a new service"""
    implements(IRegisteredService)

    meta_type = "RegisteredService"
    schema = RegisteredServiceSchema

    def getScopeValues(self, asString = 0):
        """Return the human readable values of the scope keys"""
        projects = self.getUsed_by_projects()
        scopes = []
        [scopes.extend(p.getScopeValues()) for p in projects]
        s = set(scopes)
        if  asString:
            return ", ".join(s)
        return s # tuple(s)


atapi.registerType(RegisteredService, PROJECTNAME)

