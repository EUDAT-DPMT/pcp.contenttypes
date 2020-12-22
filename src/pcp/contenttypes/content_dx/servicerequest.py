from pcp.contenttypes.backrels.backrelfield import BackrelField
from pcp.contenttypes.content_dx.common import RequestUtilities
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope.interface import implementer


class IServiceRequest(model.Schema):
    """Dexterity Schema for ServiceRequest"""

    service = RelationChoice(
        title='Service',
        description='The service being requested',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['service_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_option = RelationChoice(
        title='Service option',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service_option',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )

    service_hours = RelationChoice(
        title='Service hours',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service_hours',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )

    registered_service = BackrelField(
        title='Registered service',
        relation='original_request',
    )

    # CommentField resource_comment


@implementer(IServiceRequest)
class ServiceRequest(Container, RequestUtilities):
    """ServiceRequest instance"""
