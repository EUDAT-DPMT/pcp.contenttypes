from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IRegisteredResource(model.Schema):
    """Dexterity Schema for RegisteredResource"""


@implementer(IRegisteredResource)
class RegisteredResource(Container):
    """RegisteredResource instance"""
