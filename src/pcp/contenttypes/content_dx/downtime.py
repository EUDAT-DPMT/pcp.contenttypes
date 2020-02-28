# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IDowntime(model.Schema):
    """Dexterity Schema for Downtimes
    """

    dexteritytextindexer.searchable(
        'startDateTime',        
        'endDateTime',
        'severity',
        'classification'
    )

    startDateTime = schema.Datetime(
            title=u'Start date (UTC)',
            description=u'When does the downtime start? In UTC!',
            required=True,
            )

    endDateTime = schema.Datetime(
            title=u'End date (UTC)',
            description=u'When does the downtime end? In UTC!',
            required=True,
            )

    #ReferenceField affected_registered_services

    reason = schema.URI(
            title=u'Reason',
            description=u'Optional URL to the change management document providing the reason for this downtime.',
            required=False,
            )

    severity = schema.TextLine(
            title=u'Severity',
            required=False,
            )

    classification = schema.TextLine(
            title=u'Classification',
            required=False,
            )
            
@implementer(IDowntime)
class Downtime(Container):
    """Downtime instance"""

