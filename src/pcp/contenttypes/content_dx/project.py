# -*- coding: UTF-8 -*-
from collective.relationhelpers import api as relapi
from pcp.contenttypes.backrels.backrelfield import BackrelField
from pcp.contenttypes.content_dx.common import CommonUtilities
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IProject(model.Schema):
    """Dexterity Schema for Projects
    """

    website = schema.URI(title=u"Website", required=False,)

    community = RelationChoice(
            title=u"Community",
            description=u"Main customer involved in this project.",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "community",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["community_dx"],
                "basePath": make_relation_root_path,
            },
        )

    community_contact = RelationChoice(
            title=u"Customer contact",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "community_contact",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["person_dx"],
                "basePath": make_relation_root_path,
            },
        )

    registered_services_used = RelationList(
            title=u"Registered services used",
            description=u"Select all registered services the project requires",
            default=[],
            value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
            missing_value=[],
            required=False,
            )
    directives.widget(
            "registered_services_used",
            RelatedItemsFieldWidget,
            vocabulary='plone.app.vocabularies.Catalog',
            pattern_options={
                "selectableTypes": ["registeredservice_dx"],
                "basePath": make_relation_root_path,
            },
        )
    # TODO: Add custom edit-form: https://community.plone.org/t/conditional-fields-in-dexterity-schema/12248/5
    # condition='python:here.stateIn(["enabling","pre_production","production","terminated"])' <-- Where does that fit?

    allocated_new = schema.TextLine(title=u'Allocated', readonly=True)

    used_new = schema.TextLine(title=u'Used', readonly=True)

    general_provider = RelationChoice(
            title=u"General provider",
            description=u"General provider for this project (chose EUDAT Ltd if in doubt)",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
    )
    directives.widget(
        "general_provider",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["provider_dx"],
            "basePath": make_relation_root_path,
        },
    )

    project_enabler = RelationChoice(
            title=u"Project enabled by",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
    )
    directives.widget(
        "project_enabler",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )
    # condition="python:here.stateNotIn(['considered'])" <-- Where does that fit?

    start_date = schema.Datetime(title=u"Start date", required=False,)
    directives.widget("start_date", DatetimeFieldWidget)

    end_date = schema.Datetime(title=u"End date", required=False,)
    directives.widget("end_date", DatetimeFieldWidget)

    call_for_collaboration = schema.URI(
        title=u"Call for collaboration",
        description=u"URL to the call that triggered this project",
        required=False,
    )

    uptake_plan = schema.URI(
        title=u"Uptake plan",
        description=u"URL to the project uptake plan (if not available on this site). Otherwise, often found on the confluence site.",
        required=False,
    )

    repository = schema.TextLine(
        title=u"Repository",
        description=u"If the data to be dealt with here are in a web-accessible repository already you should specify its URL here.",
        required=False,
    )

    topics = schema.TextLine(
        title=u"Topics",
        description=u"Please mention the scientific field(s) the data originate from.",
        required=False,
    )

    directives.widget(scopes=CheckBoxFieldWidget)
    scopes = schema.List(
        title=u'Scope',
        description=u'Tick all that apply. If in doubt, select "EUDAT".',
        value_type=schema.Choice(vocabulary='dpmt.scope_vocabulary'),
        missing_value=[],
        required=True,
    )

    resources = BackrelField(
        title=u'Resources',
        relation='project',
    )

    resource_usage = schema.TextLine(title=u'Resource usage', readonly=True)

    registered_objects = schema.TextLine(title=u'Registered objects', readonly=True)


@implementer(IProject)
class Project(Container, CommonUtilities):
    """Project instance"""

    def get_resources(self):
        resources = relapi.get_relations(self, 'customer', backrefs=True, fullobj=True) or []
        return [i['fullobj'] for i in resources]

    @property
    def resource_usage(self):
        return self.listResourceUsage(self.get_resources())

    @property
    def registered_objects(self):
        return self.registeredObjectsTotal()

    @property
    def allocated_new(self):
        return self.renderMemoryValue(self.convert(self.getStorageResourcesSizeSummary(self.get_resources())))

    @property
    def used_new(self):
        return self.renderMemoryValue(self.convert(self.getStorageResourcesUsedSummary(self.get_resources())))
