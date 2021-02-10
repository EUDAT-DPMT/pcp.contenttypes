from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from pcp.contenttypes.backrels.backrelfield import BackrelField
from pcp.contenttypes.content_dx.common import CommonUtilities
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.app.z3cform.widget import DateFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IProject(model.Schema):
    """Dexterity Schema for Projects"""

    dexteritytextindexer.searchable(
        'website',
        'community',
        'community_contact',
        'registered_services_used',
        'general_provider',
        'project_enabler',
        'call_for_collaboration',
        'uptake_plan',
        'repository',
        'topics',
        'scopes',
        'resources',
    )

    website = schema.URI(
        title='Website',
        required=False,
    )

    community = RelationChoice(
        title='Customer',
        description='Main customer involved in this project.',
        vocabulary=StaticCatalogVocabulary({'portal_type': 'community_dx'}),
        required=False,
    )
    directives.widget(
        'community',
        SelectFieldWidget,
    )

    community_contact = RelationChoice(
        title='Customer contact',
        vocabulary=StaticCatalogVocabulary({'portal_type': 'person_dx'}),
        required=False,
    )
    directives.widget(
        'community_contact',
        SelectFieldWidget,
    )

    registered_services_used = RelationList(
        title='Registered services used',
        description='Select all registered services the project requires',
        default=[],
        value_type=RelationChoice(
            vocabulary=StaticCatalogVocabulary({'portal_type': 'registeredservice_dx'}),
        ),
        missing_value=[],
        required=False,
    )
    directives.widget(
        'registered_services_used',
        SelectFieldWidget,
    )
    # TODO: Add custom edit-form: https://community.plone.org/t/conditional-fields-in-dexterity-schema/12248/5
    # condition='python:here.stateIn(["enabling","pre_production","production","terminated"])' <-- Where does that fit?

    allocated_new = schema.TextLine(title='Allocated', readonly=True)

    used_new = schema.TextLine(title='Used', readonly=True)

    general_provider = RelationChoice(
        title='General provider',
        description='General provider for this project (chose EUDAT Ltd if in doubt)',
        vocabulary=StaticCatalogVocabulary({'portal_type': 'provider_dx'}),
        required=False,
    )
    directives.widget(
        'general_provider',
        SelectFieldWidget,
    )

    project_enabler = RelationChoice(
        title='Project enabled by',
        vocabulary=StaticCatalogVocabulary({'portal_type': 'person_dx'}),
        required=False,
    )
    directives.widget(
        'project_enabler',
        SelectFieldWidget,
    )
    # condition="python:here.stateNotIn(['considered'])" <-- Where does that fit?

    start_date = schema.Date(
        title='Start date',
        required=False,
    )
    directives.widget('start_date', DateFieldWidget)

    end_date = schema.Date(
        title='End date',
        required=False,
    )
    directives.widget('end_date', DateFieldWidget)

    call_for_collaboration = schema.URI(
        title='Call for collaboration',
        description='URL to the call that triggered this project',
        required=False,
    )

    uptake_plan = schema.URI(
        title='Uptake plan',
        description='URL to the project uptake plan (if not available on this site). Otherwise, often found on the confluence site.',
        required=False,
    )

    repository = schema.TextLine(
        title='Repository',
        description='If the data to be dealt with here are in a web-accessible repository already you should specify its URL here.',
        required=False,
    )

    topics = schema.TextLine(
        title='Topics',
        description='Please mention the scientific field(s) the data originate from.',
        required=False,
    )

    directives.widget(scopes=CheckBoxFieldWidget)
    scopes = schema.List(
        title='Scope',
        description='Tick all that apply. If in doubt, select "EUDAT".',
        value_type=schema.Choice(vocabulary='dpmt.scope_vocabulary'),
        missing_value=[],
        default=[],
        required=True,
    )

    resources = BackrelField(
        title='Resources',
        relation='project',
    )

    resource_usage = schema.TextLine(title='Resource usage', readonly=True)

    registered_objects = schema.TextLine(title='Registered objects', readonly=True)


@implementer(IProject)
class Project(Container, CommonUtilities):
    """Project instance"""

    def get_resources(self):
        return relapi.backrelations(self, 'customer')

    @property
    def resource_usage(self):
        return self.listResourceUsage(self.get_resources())

    @property
    def registered_objects(self):
        return self.registeredObjectsTotal()

    @property
    def allocated_new(self):
        return self.renderMemoryValue(
            self.convert(self.getStorageResourcesSizeSummary(self.get_resources()))
        )

    @property
    def used_new(self):
        return self.renderMemoryValue(
            self.convert(self.getStorageResourcesUsedSummary(self.get_resources()))
        )

    def getScopeValues(self, asString=False):
        """Return the human readable values of the scope keys"""
        # BBB
        scopes = list(self.scopes)
        if asString:
            return ', '.join(scopes)
        else:
            return scopes
