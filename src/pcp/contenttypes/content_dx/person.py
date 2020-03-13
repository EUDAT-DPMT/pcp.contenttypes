# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
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


class IPerson(model.Schema):
    """Dexterity Schema for Persons
    """

    # Formattable name field 'name'
    # Email field 'email'

    affiliation = RelationChoice(
        title=u"Affiliation",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False, 
    )
    directives.widget(
        "affiliation",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["provider_dx","community_dx"],
            "basePath": make_relation_root_path,
        },
    )

    # Phone numbers field 'phone'
    # Back reference field 'manages'
    # Back reference field 'provider_contact_for'
    # Back reference field 'business_contact_for'
    # Back reference field 'security_contact_for'
    # Back reference field 'provider_admin'
    # Back reference field 'she_contact'
    # Back reference field 'community_contact_for'
    # Back reference field 'community_representative'
    # Back reference field 'community_admin'
    # Back reference field 'enables'
    # Back reference field 'service_owner_of'
    # Back reference field 'principal_investigator_of'
    # Back reference field 'manager_of_registered_service'


# Item or Container?
@implementer(IPerson)
class Person(Container):
    """Person instance"""
