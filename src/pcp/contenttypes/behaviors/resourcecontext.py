"""DPMT Resource context behaviour

Includes form fields to describe the context of a resource
"""

from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


@provider(IFormFieldProvider)
class IDPMTResourceContext(model.Schema):
    """Add fields to describe the context of a resource
    """


    services = RelationList(
        title=u"Services(s)",
        description=u"Registered service(s) or service component(s) "\
        u"through which this resource can be accessed.",
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'services',
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["registeredservice_dx",
                                "registeredservicecomponent_dx"],
            "basePath": make_relation_root_path,
        },
    )



