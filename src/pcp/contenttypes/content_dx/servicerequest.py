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

class IServiceRequest(model.Schema):
    """Dexterity Schema for ServiceRequest
    """

    service = RelationChoice(
        title=u"Service",
        description=u"The service being requested",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["service_dx"],
            "basePath": make_relation_root_path,
        },
    )

    service_option = RelationChoice(
        title=u"Service option",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service_option",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )

    service_hours = RelationChoice(
        title=u"Service hours",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "service_hours",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["Document"],
            "basePath": make_relation_root_path,
        },
    )   

    registered_service = BackrelField(
        title=u'Registered service',
        relation='original_request',
        )

    # CommentField resource_comment


@implementer(IServiceRequest)
class ServiceRequest(Container):
    """ServiceRequest instance"""
