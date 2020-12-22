from collective import dexteritytextindexer
from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IService(model.Schema):
    """Dexterity Schema for Services"""

    dexteritytextindexer.searchable(
        'url',
        'service_area',
        'service_type',
        'value_to_customer',
        'risks',
        'funders_for_service',
        'request_procedures',
        'helpdesk',
    )

    description_internal = schema.TextLine(
        title='Internal description',
        required=False,
    )

    url = schema.URI(
        title='Url',
        required=False,
    )

    service_area = schema.TextLine(
        title='Service area',
        required=False,
    )

    service_type = schema.TextLine(
        title='Service type',
        required=False,
    )

    value_to_customer = schema.TextLine(
        title='Value to customer',
        required=False,
    )

    risks = schema.TextLine(
        title='Risks',
        required=False,
    )

    funders_for_service = schema.TextLine(
        title='Funders',
        description='Funders for this service',
        required=False,
    )

    request_procedures = schema.TextLine(
        title='Request procedures',
        required=False,
    )

    helpdesk = schema.URI(
        title='Helpdesk',
        required=False,
    )

    managed_by = RelationChoice(
        title='Managed by',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'managed_by',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_owner = RelationChoice(
        title='Service owner',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'service_owner',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    contact = RelationChoice(
        title='Contact',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'contact',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['person_dx'],
            'basePath': make_relation_root_path,
        },
    )

    service_complete_link = schema.URI(
        title='Link to SPMT',
        required=False,
    )
    # ateapi.UrlField
    # read_permission='View internals',
    # write_permission='Modify internals',

    competitors = schema.TextLine(
        title='Competitors',
        required=False,
    )
    # read_permission='View internals',
    # write_permission='Modify internals',
    # macro_view='trusted_string',

    resources_used = BackrelField(
        title='Resources used',
        relation='used_by',
        # invisible
    )

    used_by_project = BackrelField(
        title='Used by projects',
        relation='using',
        # invisible
    )

    offered_by = BackrelField(
        title='Offered by',
        relation='service_offered',
        # invisible
    )

    service_requests = BackrelField(
        title='Service requests',
        relation='service',
        # invisible
    )


@implementer(IService)
class Service(Container):
    """Service instance"""
