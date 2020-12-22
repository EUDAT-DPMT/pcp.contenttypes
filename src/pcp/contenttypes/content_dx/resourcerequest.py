from collective import dexteritytextindexer
from pcp.contenttypes.content_dx.common import RequestUtilities
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IResourceRequest(model.Schema):
    """Dexterity Schema for ResourceRequest"""


@implementer(IResourceRequest)
class ResourceRequest(Container, RequestUtilities):
    """ResourceRequest instance"""
