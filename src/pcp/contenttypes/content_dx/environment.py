# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IEnvironment(model.Schema):
    """Dexterity Schema for Providers
    """

    # ReferenceField contact

    account = schema.TextLine(title=u"Account", required=False,)

    terms_of_use = schema.URI(title=u"Terms of Use", required=False,)

    rootaccess = schema.Bool(title=u"Root Access", required=False,)

    setup_procedure = schema.TextLine(title=u"Setup Procedure", required=False,)

    firewall_policy = schema.TextLine(title=u"Firewall Policy", required=False,)


@implementer(IEnvironment)
class Environment(Container):
    """Environment instance"""
