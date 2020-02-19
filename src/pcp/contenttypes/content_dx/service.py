# -*- coding: UTF-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IService(model.Schema):
    """Dexterity Schema for Services
    """

    description_internal = schema.TextLine(
        title=u'Internal description',
        required=False,
        )


@implementer(IService)
class Service(Container):
    """Service instance"""
