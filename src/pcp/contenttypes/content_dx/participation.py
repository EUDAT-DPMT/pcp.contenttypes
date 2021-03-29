from collective import dexteritytextindexer
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IParticipation(model.Schema):
    """Dexterity Schema for Participations"""

    dexteritytextindexer.searchable(
        'effort',
    )

    effort = schema.TextLine(
        title='Effort',
        required=False,
    )

    start_date = schema.Date(
        title='Start date',
        required=False,
    )
    directives.widget('start_date', DateFieldWidget)

    end_date = schema.Date(
        title='End date',
        required=False,
    )
    directives.widget('end_date', DateFieldWidget)

@implementer(IParticipation)
class Participation(Container):
    """Participation instance"""
