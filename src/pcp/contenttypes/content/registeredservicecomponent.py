"""Definition of the RegisteredServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATExtensions import ateapi

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

RegisteredServiceComponentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
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
                      widget=atapi.StringWidget(label='Service type',
                                            ),
                  ), # should there be a controlled vocabulary for this?
    atapi.StringField('service_url',
                      searchable=1,
                      widget=atapi.StringWidget(label='Service URL',
                                                description='[http|https|irods|gsiftp|ssh]://URL:port',
                                            ),
                  ),
    BackReferenceField('parent_services',
                       relationship='service_components',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
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
                                                description="Host's IP6 address "\
                                                "(0000:0000:0000:0000:0000:0000:0000:0000[/int])"\
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
)) + CommonFields.copy()


schemata.finalizeATCTSchema(RegisteredServiceComponentSchema, moveDiscussion=False)


class RegisteredServiceComponent(base.ATCTContent, CommonUtilities):
    """A CDI admin registers a new service component"""
    implements(IRegisteredServiceComponent)

    meta_type = "RegisteredServiceComponent"
    schema = RegisteredServiceComponentSchema

atapi.registerType(RegisteredServiceComponent, PROJECTNAME)
