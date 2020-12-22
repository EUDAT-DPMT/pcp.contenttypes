from collective.relationhelpers import api as relapi
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


class IRegisteredService(model.Schema):
    """Dexterity Schema for Registered services"""

    general_provider = RelationChoice(
        title='General provider',
        description='General provider for this project (chose EUDAT Ltd if in doubt)',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'general_provider',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['provider_dx'],
            'basePath': make_relation_root_path,
        },
    )

    contact = RelationChoice(
        title='Contact',
        description='The person responsible for this registered service.',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'contact',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    managers = RelationList(
        title='Manager(s)',
        description='Other people who can change access rights and similar critical controls.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'managers',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    monitored = schema.Bool(
        title='Monitored',
        description='Should this service be monitored?',
        required=False,
    )

    service_components = RelationList(
        title='Service components',
        description='The service components providing the service.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'service_components',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['registeredservicecomponent_dx'],
            'basePath': make_relation_root_path,
        },
    )

    original_request = RelationChoice(
        title='Request',
        description='The original request that triggered the establishment of this service.',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'original_request',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['servicerequest_dx'],
            'basePath': make_relation_root_path,
        },
    )

    registry_link = schema.TextLine(title='Central Registry', readonly=True)

    used_by_projects = BackrelField(
        title='Used by project',
        relation='registered_services_used',
    )

    scopes = schema.TextLine(title='Project Scopes', readonly=True)

    resources = BackrelField(
        title='Registered service\'s resources',
        relation='services',
    )


@implementer(IRegisteredService)
class RegisteredService(Container):
    """RegisteredService instance"""

    @property
    def registry_link(self):
        return self.getCregURL()

    @property
    def scopes(self):
        return self.getScopeValues(asString=True)

    def getScopeValues(self, asString=False):
        """Return the human readable values of the scope keys"""
        projects = relapi.get_backrelations(
            self, 'registered_services_used', fullobj=True
        )
        scopes = []
        [scopes.extend(p['fullobj'].getScopeValues()) for p in projects]
        s = set(scopes)
        if asString:
            return ', '.join(s)
        return s  # tuple(s)
