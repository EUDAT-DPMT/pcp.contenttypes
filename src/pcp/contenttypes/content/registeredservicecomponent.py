"""Definition of the RegisteredServiceComponent content type
"""

import semantic_version

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.ATExtensions import ateapi

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

RegisteredServiceComponentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.ReferenceField('service_component_implementation_details',
                         accessor='getServiceComponentImplementationDetails',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='implemented_by',
                         allowed_types=('ServiceComponentImplementationDetails',),
                         multiValued=False,
                         widget=ReferenceBrowserWidget(label='Service Component Implementation Details',
                                                       description='Reference to specific implementation Details',
                                                       searchable=True,
                                                       allow_browse=1,
                                                       startup_directory='/catalog',
                                                       show_review_state=True,
                                                       show_path=True,
                                                       ),
                         ),
    atapi.ReferenceField('service_providers',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='provided_by',
                         allowed_types=('Provider',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Service provider(s)',
                                                       description='The provider(s) hosting this service component.',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                       ),
                         ),
    atapi.ReferenceField('contacts',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='contact_for',
                         allowed_types=('Person',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Contact(s)',
                                                       description='Contact person(s) for this specific component.',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.StringField('service_type',
                      searchable=1,
                      vocabulary=NamedVocabulary('service_types'),
                      widget=atapi.SelectionWidget(label='Service type',
                                                   ),
                      ),
    atapi.StringField('service_url',
                      searchable=1,
                      widget=atapi.StringWidget(label='Service URL',
                                                description='[http|https|irods|gsiftp|ssh]://URL:port',
                                                ),
                      ),
    BackReferenceField('parent_services',
                       relationship='service_components',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit': 'invisible'},
                                                  label='Part of these services',
                                                  ),
                       ),
    atapi.StringField('host_name',
                      searchable=1,
                      widget=atapi.StringWidget(label='Host name',
                                                description='In valid FQDN format (fully qualified domain name)',
                                                ),
                      ),
    atapi.StringField('host_ip4',
                      widget=atapi.StringWidget(label="IP4 address",
                                                description="Host's IP4 address (a.b.c.d)",
                                                ),
                      ),
    atapi.StringField('host_ip6',
                      widget=atapi.StringWidget(label="IP6 address",
                                                description="Host's IP6 address "
                                                "(0000:0000:0000:0000:0000:0000:0000:0000[/int])"
                                                "(optional [/int] range)",
                                                ),
                      ),
    atapi.StringField('host_dn',
                      searchable=1,
                      widget=atapi.StringWidget(label="Distinguished name (DN)",
                                                description="Host's DN (/C=.../OU=...?...)",
                                                ),
                      ),
    atapi.StringField('host_os',
                      searchable=1,
                      widget=atapi.StringWidget(label='Host operating system',
                                                description='Alphanumeric and basic punctuation',
                                                ),
                      ),
    atapi.StringField('host_architecture',
                      searchable=1,
                      widget=atapi.StringWidget(label='Host architecture',
                                                description='Alphanumeric and basic punctuation',
                                                ),
                      ),
    atapi.BooleanField('monitored'),
    atapi.ComputedField('registry_link',
                        expression='here.getCregURL()',
                        widget=atapi.ComputedWidget(label='Central Registry'),
                        ),
    ateapi.RecordsField('implementation_configuration',
                        accessor='getImplementationConfiguration',
                        mutator='setImplementationConfiguration',
                        schemata='details',
                        read_permission='View internals',
                        write_permission='Modify internals',
                        searchable=0,
                        subfields=('key', 'value'),
                        minimalSize=3,
                        subfield_sizes={'key': 15,
                                        },
                        innerJoin=': ',
                        outerJoin='<br />',
                        widget=ateapi.RecordsWidget(
                            label='Implementation configuration',
                            description='Implementation specific configuration according to the referenced component details implementation',
                            condition="python:here.stateNotIn(['considered'])",
                        ),
                        ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    RegisteredServiceComponentSchema, moveDiscussion=False)


class RegisteredServiceComponent(base.ATCTContent, CommonUtilities):
    """A CDI admin registers a new service component"""
    implements(IRegisteredServiceComponent)

    meta_type = "RegisteredServiceComponent"
    schema = RegisteredServiceComponentSchema

    def at_post_edit_script(self):

        # check for a reference to a ServiceComponentImplementDetails object
        scid = self.getServiceComponentImplementationDetails()
        if scid:
            # obtain its configuration parameters configuration
            configuration_parameters = sorted(scid.getField('configuration_parameters').get(scid))

            # get hold of the related records field from the current object
            implementation_configuration = self.getImplementationConfiguration()
            # dictify its records
            existing_records = dict([(d['key'], d.get('value', '')) for d in implementation_configuration])

            # build a new record structure based on the master configuration parameters
            # and the existing values

            result = list()
            for key in configuration_parameters:
                result.append(dict(
                    key=key,
                    value=existing_records.get(key, '')))
            self.setImplementationConfiguration(result)

    def check_versions(self):
        """ Check if references service_component_implement_details reference
            is up-to-date.
        """

        scid = self.getServiceComponentImplementationDetails()
        if not scid:
            return

        # get parent ServiceComponentImplementation
        sci = scid.aq_parent
        available_implementations = sci.contentValues()
        available_implementations = sorted(available_implementations, key=lambda item: semantic_version.Version(item.getVersion()))
        latest_version = None
        latest_version_url = None
        if available_implementations:
            latest_version = available_implementations[-1].getVersion()
            latest_version_url = available_implementations[-1].absolute_url()

        return dict(
                is_current=latest_version==scid.getVersion(),
                current_version=scid.getVersion(),
                current_version_url=scid.absolute_url(),
                latest_version=latest_version,
                latest_version_url=latest_version_url,
                available_implementations=available_implementations)


atapi.registerType(RegisteredServiceComponent, PROJECTNAME)
