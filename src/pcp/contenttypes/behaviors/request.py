"""DPMT Request behaviour

Includes form fields common to all request types
"""

from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.textfield import RichText
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IDPMTRequest(model.Schema):
    """Add fields common to all request types"""

    startDate = schema.Datetime(
        title='Start date',
        description='Until when does the request need to be realized?',
        required=False,
    )
    directives.widget('startDate', DatetimeFieldWidget)

    endDate = schema.Datetime(
        title='End date',
        description='If know: the time when this can be decommissioned.',
        required=False,
    )
    directives.widget('endDate', DatetimeFieldWidget)

    preferred_providers = RelationList(
        title='Preferred provider(s)',
        description='If there is a reason to prefer certain '
        'provider(s) this can be specified here. Usually '
        'this can be left empty.',
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'preferred_providers',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            'selectableTypes': ['provider_dx'],
            'basePath': make_relation_root_path,
        },
    )

    ticketid = schema.TextLine(
        title='Ticket ID',
        description="Once a ticket in EUDAT's Trouble Ticket "
        'System (TTS) has been created its ID can be entered '
        'here for easy reference.',
        required=False,
    )
