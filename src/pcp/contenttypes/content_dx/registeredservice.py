# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IRegisteredService(model.Schema):
    """Dexterity Schema for Registered services
    """
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

    contact = RelationChoice(
        title=u"Contact",
        description=u"The person responsible for this registered service.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "contact",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    managers = RelationList(
        title=u"Manager(s)",
        description=u"Other people who can change access rights and similar critical controls.",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "managers",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    monitored = schema.Bool(
        title=u"Monitored",
        description=u"Should this service be monitored?",
        required=False,
    )

    service_components = RelationList(
        title=u"Service components",
        description=u"The service components providing the service.",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "service_components",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["registeredservicecomponent_dx"],
            "basePath": make_relation_root_path,
        },
    )

    original_request = RelationChoice(
        title=u"Request",
        description=u"The original request that triggered the establishment of this service.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "original_request",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["servicerequest_dx"],
            "basePath": make_relation_root_path,
        },
    )

    registry_link = schema.TextLine(title=u'Central Registry', readonly=True)

    used_by_projects = BackrelField(
        title=u'Used by project',
        relation='registered_services_used',
        )

    scopes = schema.TextLine(title=u'Project Scopes', readonly=True)

    resources = BackrelField(
        title=u'Registered service\'s resources',
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
        projects = relapi.backrelations(self, 'services')
        scopes = []
        [scopes.extend(p.getScopeValues()) for p in projects]
        s = set(scopes)
        if asString:
            return u', '.join(s)
        return s  # tuple(s)
