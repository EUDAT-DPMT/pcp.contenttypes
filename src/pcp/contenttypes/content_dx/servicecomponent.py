from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IServiceComponent(model.Schema):
    """Dexterity Schema for ServiceComponent"""

    offered_by = BackrelField(
        title='Offered by',
        relation='service_component_offered',
    )

    requested_by = BackrelField(
        title='Requested by',
        relation='requested_component',
    )


@implementer(IServiceComponent)
class ServiceComponent(Container):
    """ServiceComponent instance"""
