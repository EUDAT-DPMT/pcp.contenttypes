"""Definition of the Provider content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProviderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url',
                    searchable=1,
                ),
    atapi.StringField('infrastructure',
                      searchable=1,
                      widget=atapi.StringWidget(label='Infrastructure status',
                                            ),
                  ),
    atapi.StringField('domain',
                      searchable=1,
                  ),
    ateapi.AddressField('address'),
    atapi.StringField('timezone'),  # from a controlled vocab maybe?
    atapi.StringField('latitude',
                      widget=atapi.StringWidget(description='If known; GOCDB can use this. '\
                                                '(-90 <= number <= 90)',
                                            ),
                  ),
    atapi.StringField('longitude',
                      widget=atapi.StringWidget(description='If known; GOCDB can use this. '\
                                                '(-180 <= number <= 180)',
                                            ),
                  ),
    atapi.StringField('ip4range',
                      widget=atapi.StringWidget(label='IPv4 range',
                                                description='(a.b.c.d/e.f.g.h)',
                                            ),
                  ),
    atapi.StringField('ip6range',
                      widget=atapi.StringWidget(label='IPv6 range',
                                                #description='(a.b.c.d/e.f.g.h)',
                                            ),
                  ),
    atapi.ReferenceField('contact',
                         relationship='contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Contact',
                                                       description='Main contact person for this provider',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('security_contact',
                         relationship='security_contact',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Security contact',
                                                       description='Person specifically to be contacted '\
                                                       'for security-related matters',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.ReferenceField('admins',
                         relationship='admin_of',
                         multiValued=True,
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Administrators',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
    atapi.StringField('emergency_phone',
                      searchable=1,
                      widget=atapi.StringWidget(label='Emergency telephone number',
                                                description='Include '\
                                                'international prefix and area code',
                                            ),
                  ),
    ateapi.EmailField('alarm_email',
                      searchable=1,
                      widget=ateapi.EmailWidget(label='Alarm E-mail',
                                                description='To be used in emergencies',
                                            ),
                      ),
    ateapi.EmailField('helpdesk_email',
                      searchable=1,
                      widget=ateapi.EmailWidget(label='Helpdesk E-mail',
                                                description='Generic helpdesk email address of this '\
                                                'provider; not specific to any service.',
                                            ),
                  ),
    atapi.LinesField('supported_os',
                     searchable=True,
                     multiValued=True,
                     vocabulary='getOSVocab',
                     widget=atapi.MultiSelectionWidget(format='checkbox'),
                     ),
    atapi.IntegerField('committed_cores', schemata='resources'),
    atapi.IntegerField('committed_disk', schemata='resources', size=20),
    atapi.IntegerField('committed_tape', schemata='resources', size=20),
    atapi.IntegerField('used_disk', schemata='resources', size=20),
    atapi.IntegerField('used_tape', schemata='resources', size=20),
    atapi.ReferenceField('communities_primary',
                         relationship='primary_provider_for',
                         multiValued=True,
                         allowed_types=('Community',),
                         widget=ReferenceBrowserWidget(label='Primary provider for',
                                                       allow_browse=1,
                                                       startup_directory='/communities',
                                                       ),
                         ),
    atapi.ReferenceField('communities_secondary',
                         relationship='secondary_provider_for',
                         multiValued=True,
                         allowed_types=('Community',),
                         widget=ReferenceBrowserWidget(label='Secondary provider for',
                                                       allow_browse=1,
                                                       startup_directory='/communities',
                                                       ),
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
    atapi.ComputedField('registry_link',
                        expression='here.getCregURL()',
                        widget=atapi.ComputedWidget(label='Central Registry'),
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
        result['url'] = self.getUrl()
        result['country'] = self.getAddress()['country']
        result['infrastructure'] = self.getInfrastructure()
        result['timezone'] = self.getTimezone()
        result['latitude'] = self.getLatitude()
        result['longitude'] = self.getLongitude()
        result['domain'] = self.getDomain()
        #result[''] = 1
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
  <SITE ID="{creg_id}" PRIMARY_KEY="{pk}" NAME="{id}">
    <PRIMARY_KEY>{pk}</PRIMARY_KEY>
    <SHORT_NAME>{id}</SHORT_NAME>
    <OFFICIAL_NAME>{description}</OFFICIAL_NAME>
    <DPMT_URL>{dpmt_url}</DPMT_URL>
    <GOCDB_PORTAL_URL>{creg_url}</GOCDB_PORTAL_URL>
    <HOME_URL>{url}</HOME_URL>
    <CONTACT_EMAIL>eudat-support@bsc.es</CONTACT_EMAIL>
    <CONTACT_TEL>+34 934 054 221</CONTACT_TEL>
    <COUNTRY_CODE>XX</COUNTRY_CODE>
    <COUNTRY>{country}</COUNTRY>
    <ROC>EUDAT_REGISTRY</ROC>
    <PRODUCTION_INFRASTRUCTURE>{infrastructure}</PRODUCTION_INFRASTRUCTURE>
    <CERTIFICATION_STATUS>Candidate</CERTIFICATION_STATUS>
    <TIMEZONE>{timezone}</TIMEZONE>
    <LATITUDE>{latitude}</LATITUDE>
    <LONGITUDE>{longitude}</LONGITUDE>
    <CSIRT_EMAIL>eudat-security@bsc.es</CSIRT_EMAIL>
    <DOMAIN>
      <DOMAIN_NAME>{domain}</DOMAIN_NAME>
    </DOMAIN>
    <EXTENSIONS>
      <EXTENSION>
        <LOCAL_ID>182</LOCAL_ID>
        <KEY>type</KEY>
        <VALUE>generic</VALUE>
      </EXTENSION>
    </EXTENSIONS>
  </SITE>
"""
atapi.registerType(Provider, PROJECTNAME)
