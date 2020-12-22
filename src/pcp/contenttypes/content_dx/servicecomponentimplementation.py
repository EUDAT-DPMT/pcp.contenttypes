from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IServiceComponentImplementation(model.Schema):
    """Dexterity Schema for ServiceComponentImplementation"""

    offered_by = BackrelField(
        title='Offered by',
        relation='service_component_implementations_offered',
    )

    requested_by = BackrelField(
        title='Requested by',
        relation='requested_component_implementations',
    )


@implementer(IServiceComponentImplementation)
class ServiceComponentImplementation(Container):
    """ServiceComponentImplementation instance"""
