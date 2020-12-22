from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IHandleEndpoint(model.Schema):
    """Dexterity Schema for Handle endpoint"""

    host = schema.TextLine(
        title='Host',
        required=False,
    )

    ip = schema.TextLine(
        title='IP',
        required=False,
    )

    monitored = schema.TextLine(
        title='Monitored',
        description='Yes or no',
        required=False,
    )

    monitoring_user = schema.TextLine(
        title='Monitoring user',
        required=False,
    )

    system_operations_user = schema.TextLine(
        title='Sytem operations user',
        required=False,
    )

    remote_user = schema.TextLine(
        title='Remote user names',
        description='Comma separated list of remote user names to be used.',
        required=False,
    )

    prefix = schema.TextLine(
        title='Prefix',
    )

    mirrored_to = RelationList(
        title='Mirror(s)',
        description='Other Handle server(s) mirroring this prefix.',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'mirrored_to',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['handleendpoint_dx'],
            'basePath': make_relation_root_path,
        },
    )

    contacts = schema.TextLine(
        title='Contacts',
        required=False,
    )

    related_project = RelationChoice(
        title='Related project',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'related_project',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['project_dx'],
            'basePath': make_relation_root_path,
        },
    )

    related_service = RelationChoice(
        title='Related service',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'related_service',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['registeredservice_dx'],
            'basePath': make_relation_root_path,
        },
    )

    text = RichText(
        title='Text',
        description='Anything else to further describe this endpoint.',
        required=False,
    )


@implementer(IHandleEndpoint)
class HandleEndpoint(Container):
    """HandleEndpoint instance"""
