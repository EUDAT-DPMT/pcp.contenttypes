# -*- coding: utf-8 -*-
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
        title=u'Host',
        required=False,
    )

    ip = schema.TextLine(
        title=u'IP',
        required=False,
    )

    monitored = schema.TextLine(
        title=u'Monitored',
        description=u'Yes or no',
        required=False,
    )

    monitoring_user = schema.TextLine(
        title=u'Monitoring user',
        required=False,
    )

    system_operations_user = schema.TextLine(
        title=u'Sytem operations user',
        required=False,
    )

    remote_user = schema.TextLine(
        title=u'Remote user names',
        description=u'Comma separated list of remote user names to be used.',
        required=False,
    )

    prefix = schema.TextLine(
        title=u'Prefix',
    )

    mirrored_to = RelationList(
        title=u'Mirror(s)',
        description=u'Other Handle server(s) mirroring this prefix.',
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
        title=u'Contacts',
        required=False,
    )

    related_project = RelationChoice(
        title=u'Related project',
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
        title=u'Related service',
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
        title=u'Text',
        description=u'Anything else to further describe this endpoint.',
        required=False,
    )


@implementer(IHandleEndpoint)
class HandleEndpoint(Container):
    """HandleEndpoint instance"""
