"""Definition of the RegisteredServiceComponent content type
"""

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

    # establish backwards compatibility with GOCDB

    def collect_data(self):
        """Helper to ccollect the values to be rendered as XML"""
        result = {}
        result['id'] = self.Title()
        result['description'] = self.Description()
        result['creg_id'] = self.getCregId()
        result['pk'] = 1
        result['dpmt_url'] = self.absolute_url()
        result['creg_url'] = self.getCregURL()
        result['service_type'] = self.getService_type()
        result['host_ip'] = self.getHost_ip4()
        result['monitored'] = self.getMonitored()
        result['url'] = self.getService_url()
        result['hostname'] = self.getHost_name()
        return result

    def xml(self, core=True, indent=2):
        """Render as XML compatible with GOCDB"""
        data = self.collect_data()
        body = gocdb_template.format(**data)
        if core:
            return body
        full = """
<?xml version="1.0" encoding="UTF-8"?>
<results>"""  + body +  """</results>"""
        return full

gocdb_template = """  
  <SERVICE_ENDPOINT PRIMARY_KEY="{pk}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <HOSTNAME>{hostname}</HOSTNAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <BETA>N</BETA>
    <SERVICE_TYPE>{service_type}</SERVICE_TYPE>
    <HOST_IP>{host_ip}</HOST_IP>
    <CORE></CORE>
    <IN_PRODUCTION>Y</IN_PRODUCTION>
    <NODE_MONITORED>{monitored}</NODE_MONITORED>
    <SITENAME>DKRZ</SITENAME>
    <COUNTRY_NAME>Germany</COUNTRY_NAME>
    <COUNTRY_CODE>DE</COUNTRY_CODE>
    <ROC_NAME>EUDAT_REGISTRY</ROC_NAME>
    <URL>{url}</URL>
    <ENDPOINTS/>
    <EXTENSIONS>
      <EXTENSION>
        <LOCAL_ID>302</LOCAL_ID>
        <KEY>epic_version</KEY>
        <VALUE>2.3</VALUE>
      </EXTENSION>
      <EXTENSION>
        <LOCAL_ID>301</LOCAL_ID>
        <KEY>handle_version</KEY>
        <VALUE>7.3.1</VALUE>
      </EXTENSION>
    </EXTENSIONS>
  </SERVICE_ENDPOINT>
"""

atapi.registerType(RegisteredServiceComponent, PROJECTNAME)
