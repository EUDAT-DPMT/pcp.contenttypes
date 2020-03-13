# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.dexterity.content import Container
from plone.supermodel import model
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
    # condition='python:here.stateIn(["enabling","pre_production","production","terminated"])' <-- Where does that fit?

    # Computed field 'allocated_new'
    # Computed field 'used_new'

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

    # Can a LinesField in an Archetype type be transfered into a List in a Dexterity type?
    # scopes = schema.List(
    #        title=u'Scope',
    #        description=u'Tick all that apply. If in doubt, select "EUDAT".',
    #        required=True,
    #        )

    # Back reference field "resources"
    # Computed field "resource usage"
    # Computed field "registered objects"


@implementer(IProject)
class Project(Container):
    """Project instance"""
