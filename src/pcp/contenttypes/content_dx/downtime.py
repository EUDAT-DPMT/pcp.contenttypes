# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
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

class IDowntime(model.Schema):
    """Dexterity Schema for Downtimes
    """

    dexteritytextindexer.searchable(
        "startDateTime", "endDateTime", "severity", "classification"
    )

    startDateTime = schema.Datetime(
        title=u"Start date (UTC)",
        description=u"When does the downtime start? In UTC!",
        required=True,
    )

    endDateTime = schema.Datetime(
        title=u"End date (UTC)",
        description=u"When does the downtime end? In UTC!",
        required=True,
    )

    affected_registered_services = RelationList(
        title=u"Affected registered services",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "affected_registered_services",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["registeredservice_dx","registeredservicecomponent_dx"],
            "basePath": make_relation_root_path,
        },
    )

    reason = schema.URI(
        title=u"Reason",
        description=u"Optional URL to the change management document providing the reason for this downtime.",
        required=False,
    )

    severity = schema.Choice(
        title=u'Severity',
        vocabulary='dpmt.severity_levels',
        required=False,
        )

    classification = schema.Choice(
        title=u'Classification',
        vocabulary='dpmt.downtime_classes',
        required=False,
        )


@implementer(IDowntime)
class Downtime(Container):
    """Downtime instance"""
