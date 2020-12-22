# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from pcp.contenttypes.content_dx.common import CommonUtilities
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


class IEnvironment(model.Schema):
    """Dexterity Schema for Environment"""

    contact = RelationChoice(
        title=u"Contact",
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

    account = schema.TextLine(
        title=u"Account",
        required=False,
    )

    terms_of_use = schema.URI(
        title=u"Terms of Use",
        required=False,
    )

    rootaccess = schema.Bool(
        title=u"Root Access",
        required=False,
    )

    setup_procedure = schema.TextLine(
        title=u"Setup Procedure",
        required=False,
    )

    firewall_policy = schema.TextLine(
        title=u"Firewall Policy",
        required=False,
    )


@implementer(IEnvironment)
class Environment(Container, CommonUtilities):
    """Environment instance"""
