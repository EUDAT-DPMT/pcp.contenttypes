from collective import dexteritytextindexer
from pcp.contenttypes.content_dx.common import OfferUtilities
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


class IServiceComponentOffer(model.Schema):
    """Dexterity Schema for ServiceComponentOffer"""

    service_component_offered = RelationChoice(
        title='Service component offered',
        description='Reference to the catalog entry of the service component being offered.',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service_component_offered',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['servicecomponent_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_component_implementations_offered = RelationList(
        title='Implementations offered',
        description='Reference to the catalog entry of the implementations(s) of the service component being offered.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'service_component_implementations_offered',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['servicecomponentimplementation_dx'],
            'basePath': make_relation_root_path,
        },
    )

    slas = RelationList(
        title='SLAs/OLAs offered',
        description='Potential Service/Operational Level Agreements under which the service component is being offered.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'slas',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )


@implementer(IServiceComponentOffer)
class ServiceComponentOffer(Container, OfferUtilities):
    """ServiceComponentOffer instance"""
