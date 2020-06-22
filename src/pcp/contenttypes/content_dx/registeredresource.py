# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IRegisteredResource(model.Schema):
    """Dexterity Schema for RegisteredResource
    """


@implementer(IRegisteredResource)
class RegisteredResource(Container):
    """RegisteredResource instance"""

    # XXX Shoud this come from a mixin class ???
    def getScopeValues(self, asString = 0):
        """Return the human readable values of the scope keys"""
        project = self.project  # XXX is this found??? project is defined in a behavior
        if project is None:
            if asString:
                return ''
            else:
                return ('',)
        scopes = []
        scopes.extend(project.getScopeValues())
        s = set(scopes)
        if  asString:
            return ", ".join(s)
        return s # tuple(s)
