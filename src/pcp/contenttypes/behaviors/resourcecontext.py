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
from plone.dexterity.interfaces import IDexterityContent
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import PathSourceBinder
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList


@provider(IFormFieldProvider)
class IDPMTResourceContext(model.Schema):
    """Add fields to describe the context of a resource
    """

    project = RelationChoice(
            title=u"Project",
            description=u"The project for which this resource is provided.",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "project",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["project_dx"],
                "basePath": make_relation_root_path,
            },
        )

# scopes (comp)
    scopes = schema.TextLine(
        title=u"Scope(s)",
        description=u"The project's scope(s) in which this resource is provided",
        required=False,
        # allow_uncommon=True,  # what's this?
    )
    directives.mode(scopes='display')

    customer = RelationChoice(
            title=u"Customer",
            description=u"Main customer for whom the resource is provided.",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "customer",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["community_dx"],
                "basePath": make_relation_root_path,
            },
        )

    contact = RelationChoice(
            title=u"Contact",
            description=u"The primary contact for this resource.",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "contact",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["person_dx"],
                "basePath": make_relation_root_path,
            },
        )

    request = RelationChoice(
            title=u"Request",
            description=u"The request that triggered the establishment of this resource.",
            vocabulary='plone.app.vocabularies.Catalog',
            required=False,
            )
    directives.widget(
            "request",
            RelatedItemsFieldWidget,
            pattern_options={
                "selectableTypes": ["resourcerequest_dx", "servicerequest_dx"],
                "basePath": make_relation_root_path,
            },
        )


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

    linked_resources = RelationList(
        title=u"Linked resources",
        description=u"Other resources linked to this resource.",
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'linked_resources', 
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["registeredresource_dx", 
                                "registeredcomputeresource_dx",
                                "registeredstorageresource_dx"],
            "basePath": make_relation_root_path,
        },
    )

# XXX how to include backlinks of the same relation as above?

@implementer(IDPMTResourceContext)
@adapter(IDexterityContent)
class DPMTResourceContext(object):
    """Support for computed fields and controlled vocabularies(?)
    """

    def __init__(self, context):
        self.context = context

    def _getScopeValues(self, asString = 0):
        """Return the human readable values of the scope keys"""
        project = self.project.to_object
        if project is None:
            if asString:
                return u''
            else:
                return (u'',)
        scopes = []
        scopes.extend(project.getScopeValues())
        s = set(scopes)
        if  asString:
            return u", ".join(s)
        return s # tuple(s)

    @property
    def scopes(self):
        return self._getScopeValues(asString=1)

    @scopes.setter
    def scopes(self, value):
        pass

    def _get_project(self):
        return self.context.project

    def _set_project(self, value):
        self.context.project = value

    project = property(_get_project, _set_project)


    def _get_customer(self):
        return self.context.customer

    def _set_customer(self, value):
        self.context.customer = value

    customer = property(_get_customer, _set_customer)


    def _get_contact(self):
        return self.context.contact

    def _set_contact(self, value):
        self.context.contact = value

    contact = property(_get_contact, _set_contact)


    def _get_request(self):
        return self.context.request

    def _set_request(self, value):
        self.context.request = value

    request= property(_get_request, _set_request)


    def _get_services(self):
        return self.context.services

    def _set_services(self, value):
        self.context.services = value

    services = property(_get_services, _set_services)


    def _get_linked_resources(self):
        return self.context.linked_resources

    def _set_linked_resources(self, value):
        self.context.linked_resources = value

    linked_resources = property(_get_linked_resources, _set_linked_resources)







class IDPMTResourceContextMarker(Interface):
    """Marker interface that will be provided by instances using the
    IDPMTResourceContext behavior.
    """
