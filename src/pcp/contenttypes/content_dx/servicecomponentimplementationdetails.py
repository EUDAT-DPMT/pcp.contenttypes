from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IServiceComponentImplementationDetails(model.Schema):
    """Dexterity Schema for ServiceComponentImplementationDetails"""


@implementer(IServiceComponentImplementationDetails)
class ServiceComponentImplementationDetails(Container):
    """ServiceComponentImplementationDetails instance"""
