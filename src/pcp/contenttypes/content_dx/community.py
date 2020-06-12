# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from pcp.contenttypes.backrels.backrelfield import BackrelField
from pcp.contenttypes.content_dx.common import CommonUtilities
from pcp.contenttypes.widgets import TrustedTextWidget
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.interfaces import IDisplayForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class ICommunity(model.Schema):
    """Dexterity Schema for Communities
    """

    dexteritytextindexer.searchable("VAT")

    url = schema.URI(title=u"Url", required=False,)

    # hide adress fields from display. instead show a condensed view from the property 'address'
    directives.omitted(IDisplayForm, 'street1', 'street2', 'zip', 'city', 'country')
    street1 = schema.TextLine(
        title=u'Street 1',
        required=False,
    )

    street2 = schema.TextLine(
        title=u'Street 2',
        required=False,
    )

    zip = schema.TextLine(
        title=u'ZIP code',
        required=False,
    )

    city = schema.TextLine(
        title=u'City',
        required=True,
    )

    country = schema.Choice(
        title=u'Country',
        vocabulary='dpmt.country_names',
        required=True,
    )

    address = schema.TextLine(title=u'Adress', readonly=True)
    directives.widget('address', TrustedTextWidget)

    VAT = schema.TextLine(title=u"VAT", required=False,)

    representative = RelationChoice(
        title=u"Representative",
        description=u"Main person representing the Customer.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "representative",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    community_admins = RelationList(
        title=u"Administrators",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "community_admins",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    affiliated = BackrelField(
        title=u'Affiliated',
        relation='affiliation',
        )

    projects_involved = BackrelField(
        title=u'Projects involved',
        description=u'Projects involving this customer',
        relation='community',
        )

    primary_provider = BackrelField(
        title=u'Primary_provider',
        relation='primary_provider_for',
        )

    secondary_provider = BackrelField(
        title=u'Secondary_provider',
        relation='secondary_provider_for',
        )

    topics = schema.TextLine(
        title=u"Topics",
        description=u"If applicable, please mention the scientific field(s) this customer is focussing on.",
        required=False,
    )

    resources = BackrelField(
        title=u'Customer\'s Resources',
        relation='customer',
        )

    usage_summary = schema.TextLine(title=u'Usage', readonly=True)

    resource_usage = schema.TextLine(title=u'Resource Usage', readonly=True)


@implementer(ICommunity)
class Community(Container, CommonUtilities):
    """Community instance"""

    @property
    def address(self):
        street = None
        if self.street1 and self.street2:
            street = u'{} {}'.format(self.street1, self.street2)
        elif self.street1 and not self.street2:
            street = self.street1
        elif not self.street1 and self.street2:
            street = self.street2

        city = u'{} {}'.format(self.zip, self.city) if self.zip else self.city
        items = [street, city, self.country]
        return u'<br />'.join(i for i in items if i)

    def get_resources(self):
        resources = relapi.get_relations(self, 'customer', backrefs=True, fullobj=True) or []
        return [i['fullobj'] for i in resources]

    @property
    def usage_summary(self):
        return self.getResourceUsageSummary(self.get_resources())

    @property
    def resource_usage(self):
        return self.listResourceUsage(self.get_resources())
