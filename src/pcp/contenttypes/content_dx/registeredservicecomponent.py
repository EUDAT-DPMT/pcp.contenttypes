from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IImplementationConfiguration(Interface):

    key = schema.TextLine(title='Key')
    value = schema.TextLine(title='Value')


class IRegisteredServiceComponent(model.Schema):
    """Dexterity Schema for Registered Service Component"""

    dexteritytextindexer.searchable(
        'service_component_implementation_details',
        'service_type',
        'service_url',
        'host_name',
        'host_dn',
        'host_os',
        'host_architecture',
        'emergency_phone',
        'alarm_email',
        'helpdesk_email',
        'supported_os',
    )

    service_component_implementation_details = RelationChoice(
        title='Service Component Implementation Details',
        description='Reference to specific implementation Details',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service_component_implementation_details',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['servicecomponentimplementationdetails_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_providers = RelationList(
        title='Service provider(s)',
        description='The provider(s) hosting this service component.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        missing_value=[],
        required=False,
    )
    directives.widget(
        'service_providers',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['provider_dx'],
            'basePath': make_relation_root_path,
        },
    )

    contacts = RelationList(
        title='Contact(s)',
        description='Contact person(s) for this specific component.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        missing_value=[],
        required=False,
    )
    directives.widget(
        'contacts',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_type = schema.Choice(
        title='Service component type',
        vocabulary='dpmt.service_types',
        required=False,
    )

    service_url = schema.TextLine(
        title='Service URL',
        description='[http|https|irods|gsiftp|ssh]://URL:port',
        required=False,
    )

    parent_services = BackrelField(
        title='Part of these registered services',
        relation='service_components',
    )

    scopes = schema.TextLine(title='Project Scopes', readonly=True)

    host_name = schema.TextLine(
        title='Host name',
        description='In valid FQDN format (fully qualified domain name)',
        required=False,
    )

    host_ip4 = schema.TextLine(
        title='IP4 address',
        description="Host's IP4 address (a.b.c.d)",
        required=False,
    )

    host_ip6 = schema.TextLine(
        title='IP6 address',
        description="Host's IP6 address (0000:0000:0000:0000:0000:0000:0000:0000[/int]) (optional [/int] range)))",
        required=False,
    )

    host_dn = schema.TextLine(
        title='Distinguished name (DN)',
        description="Host's DN (/C=.../OU=...?...)",
        required=False,
    )

    host_os = schema.TextLine(
        title='Host operating system',
        description='Alphanumeric and basic punctuation',
        required=False,
    )

    host_architecture = schema.TextLine(
        title='Host_architecture',
        description='Alphanumeric and basic punctuation',
        required=False,
    )

    monitored = schema.Bool(
        title='Monitored',
        required=False,
    )

    registrylink = schema.TextLine(title='Central Registry', readonly=True)

    implementation_configuration = schema.List(
        title='Implementation configuration',
        description='Implementation specific configuration according to the referenced component details implementation',
        value_type=DictRow(schema=IImplementationConfiguration),
        required=False,
        missing_value=[],
    )
    directives.widget('implementation_configuration', DataGridFieldFactory)
    # TODO: Add custom form with condition="python:here.stateNotIn(['considered'])",

    resources = BackrelField(
        title="Registered service component's resources",
        relation='services',
    )


@implementer(IRegisteredServiceComponent)
class RegisteredServiceComponent(Container):
    """RegisteredServiceComponent instance"""

    @property
    def scopes(self):
        return self.getScopeValues(asString=1)

    def getScopeValues(self, asString=0):
        """Return the human readable values of the scope keys"""
        parent_services = relapi.get_backrelations(
            self, 'service_components', fullobj=True
        )
        projects = []
        for parent_service in parent_services:
            p_service = parent_service['fullobj']
            projects.extend(
                relapi.get_backrelations(
                    p_service, 'registered_services_used', fullobj=True
                )
            )

        scopes = []
        [scopes.extend(p['fullobj'].scopes) for p in projects]
        s = set(scopes)
        if asString:
            return ', '.join(s)
        return s  # tuple(s)

    @property
    def registrylink(self):
        return self.getCregURL()
