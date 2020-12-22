"""Constraints behaviour for DPMT content types.

Includes form fields and behaviour adapters that allow the
specification of constraints where necessary
"""

from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IDPMTConstraints(model.Schema):
    """Add fields to specify constraints"""

    fieldset(
        'constraints',
        label=u'Constraints',
        fields=(
            'regional_constraints',
            'thematic_constraints',
            'organizational_constraints',
            'constraints',
        ),
    )

    regional_constraints = schema.TextLine(
        title=u"Regional constraints",
        description=u"Does the customer need to be in a certain "
        "country or region? If so, which one(s)",
        required=False,
    )

    thematic_constraints = schema.TextLine(
        title=u"Thematic constraints",
        description=u"Does the customer need to active in a certain "
        "scientific field? If so, which one(s)",
        required=False,
    )

    organizational_constraints = schema.TextLine(
        title=u"Organizational constraints",
        description=u"Does the customer need to be of a certain "
        "organizational type? If so, which one(s)",
        required=False,
    )

    constraints = RichText(
        title=u"Constraints",
        description=u"Any other constraints not yet covered.",
        required=False,
    )
