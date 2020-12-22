from pcp.contenttypes.content_dx.common import RequestUtilities
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IResourceRequest(model.Schema):
    """Dexterity Schema for ResourceRequest"""


@implementer(IResourceRequest)
class ResourceRequest(Container, RequestUtilities):
    """ResourceRequest instance"""
