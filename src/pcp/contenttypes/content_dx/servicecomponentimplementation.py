# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
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


class IServiceComponentImplementation(model.Schema):
    """Dexterity Schema for ServiceComponentImplementation"""

    offered_by = BackrelField(
        title=u'Offered by',
        relation='service_component_implementations_offered',
    )

    requested_by = BackrelField(
        title=u'Requested by',
        relation='requested_component_implementations',
    )


@implementer(IServiceComponentImplementation)
class ServiceComponentImplementation(Container):
    """ServiceComponentImplementation instance"""
