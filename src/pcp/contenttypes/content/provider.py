"""Definition of the Provider content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATExtensions import ateapi
from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

#from Products.UserField import UserField

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IProvider
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


ProviderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    ateapi.UrlField('url',
                    searchable=1,
                    ),
    atapi.ComputedField('link2offers',
                        expression="here.getOffersURL()",
                        widget=atapi.ComputedWidget(label="Resource offers"),
                        ),
    atapi.StringField('provider_type',
                      searchable=1,
                      vocabulary='provider_types',
                      default='generic',
                      widget=atapi.SelectionWidget(label='Provider type',
                                                   ),
                      ),
    atapi.StringField('provider_userid',
                    required=True,
                      searchable=0,
                      default='',
                      widget=atapi.StringWidget(label='Provider User ID',
                                                   description='User ID in Plone and accounting server',
                                                   ),
                      ),
    atapi.StringField('provider_status',
                      searchable=1,
                      vocabulary='provider_stati',
                      widget=atapi.SelectionWidget(label='Provider status',
                                                   ),
                      ),
    atapi.StringField('status_details',
                      searchable=1,
                      widget=atapi.StringWidget(label='Status details/comment',
                                                ),
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
                      widget=atapi.StringWidget(description='If known; GOCDB can use this. '
                                                '(-90 <= number <= 90)',
                                                ),
                      ),
    atapi.StringField('longitude',
                      widget=atapi.StringWidget(description='If known; GOCDB can use this. '
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
                                                # description='(a.b.c.d/e.f.g.h)',
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
                                                       description='Person specifically to be contacted '
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
                                                description='Include '
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
                                                description='Generic helpdesk email address of this '
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
                       widget=BackReferenceWidget(visible={'edit': 'invisible'},
                                                  ),
                       ),
    BackReferenceField('hosts',
                       relationship='hosted_by',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit': 'invisible'},
                                                  ),
                       ),
    BackReferenceField('projects_invloved',
                       relationship='provided_by',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Projects involved',
                                                  visible={
                                                      'edit': 'invisible'},
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
    #    UserField('site_managers',
    #              multiValued=True,
    #              localrole='CDI Manager',
    #              cumulative=True,
    #          ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    ProviderSchema,
    folderish=True,
    moveDiscussion=False
)

ProviderSchema['committed_cores'].widget.condition = 'object/show_all'
ProviderSchema['supported_os'].widget.condition = 'object/show_all'
ProviderSchema['committed_disk'].widget.condition = 'object/show_all'
ProviderSchema['committed_tape'].widget.condition = 'object/show_all'
ProviderSchema['used_disk'].widget.condition = 'object/show_all'
ProviderSchema['used_tape'].widget.condition = 'object/show_all'


class Provider(folder.ATFolder, CommonUtilities):
    """Compute or data service provider"""
    implements(IProvider)

    meta_type = "Provider"
    schema = ProviderSchema

    def getOSVocab(self):
        """provides the vocabulary for the 'supported_os' field"""

        return ateapi.getDisplayList(self, 'operating_systems', add_select=False)

    def provider_types(self):
        """provides the vocabulary for the 'provider_type' field"""

        return ateapi.getDisplayList(self, 'provider_types', add_select=False)

    def provider_stati(self):
        """provides the vocabulary for the 'provider_status' field"""

        return ateapi.getDisplayList(self, 'provider_stati', add_select=False)

    def getOffersURL(self):
        """URL to the resource offers embedded in an anchor tag.
        Used by the computed field 'offers'."""
        try:
            offers = self.offers
        except AttributeError:
            return "No offers found"
        url = offers.absolute_url()
        title = "Resources offered by %s" % self.Title()
        anchor = "<a href='%s?unit=TiB' title='%s'>%s</a>" % (
            url, title, title)
        return anchor

    def show_all(self):
        """Used in widget condition to suppress some fields in default view"""
        try:
            self.REQUEST['show_all']
            return True
        except KeyError:
            return False

    def getProvider(self):
        """ Return provider in aquisition chain """
        return self

atapi.registerType(Provider, PROJECTNAME)
