from pcp.contenttypes.content_dx.common import OfferUtilities
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IResourceOffer(model.Schema):
    """Dexterity Schema for ResourceOffer"""


@implementer(IResourceOffer)
class ResourceOffer(Container, OfferUtilities):
    """ResourceOffer instance"""
