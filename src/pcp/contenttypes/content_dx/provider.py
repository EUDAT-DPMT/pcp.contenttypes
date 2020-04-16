# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from pcp.contenttypes.content_dx.common import CommonUtilities
from pcp.contenttypes.widgets import TrustedTextWidget
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IProvider(model.Schema):
    """Dexterity Schema for Providers
    """

    dexteritytextindexer.searchable(
        "url",
        "provider_type",
        "provider_status",
        "status_details",
        "infrastructure",
        "domain",
        "VAT",
        "emergency_phone",
        "alarm_email",
        "helpdesk_email",
        "supported_os",
    )

    url = schema.URI(title=u"Url", required=False)

    link2offers = schema.TextLine(readonly=True)
    directives.widget('link2offers', TrustedTextWidget)

    directives.widget(provider_type=RadioFieldWidget)
    provider_type = schema.Choice(
        title=u'Provider type',
        vocabulary='dpmt.provider_types',
        required=False,
        )

    provider_userid = schema.TextLine(title=u"Provider user ID", required=True)

    provider_status = schema.Choice(
        title=u'Provider status',
        vocabulary='dpmt.provider_stati',
        required=False,
        )

    status_details = schema.TextLine(title=u"Status details/comment", required=False)

    infrastructure = schema.TextLine(title=u"Infrastructure", required=False)

    domain = schema.TextLine(title=u"Domain", required=False)

    # Address field

    VAT = schema.TextLine(title=u"VAT", required=False)

    timezone = schema.TextLine(title=u"Time zone", required=False)

    latitude = schema.TextLine(
        title=u"Latitude",
        description=u"If known; GOCDB can use this. (-90 <= number <= 90)",
        required=False,
    )

    longitude = schema.TextLine(
        title=u"Longitude",
        description=u"If known; GOCDB can use this. (-180 <= number <= 180)",
        required=False,
    )

    ip4range = schema.TextLine(
        title=u"IPv4 range", description=u"(a.b.c.d/e.f.g.h)", required=False
    )

    ip6range = schema.TextLine(title=u"IPv6 range", required=False)

    contact = RelationChoice(
        title=u"Contact",
        description=u"Main contact person for the operations of this provider.",
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

    business_contact = RelationChoice(
        title=u"Business contact",
        description=u"Main contact person for the financial matters of this provider.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "business_contact",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    security_contact = RelationChoice(
        title=u"Security contact",
        description=u"Person specifically to be contacted for security-related matters.",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "security_contact",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    admins = RelationList(
        title=u"Administrators",
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        "admins",
        RelatedItemsFieldWidget,
        vocabulary='plone.app.vocabularies.Catalog',
        pattern_options={
            "selectableTypes": ["person_dx"],
            "basePath": make_relation_root_path,
        },
    )

    emergency_phone = schema.TextLine(
        title=u"Emergency telephone number",
        description=u"Include international prefix and area code",
        required=False,
    )

#    alarm_email = schema.EMail(
#        title=u"Alarm E-mail",
#        description=u"To be used in emergencies",
#        required=False,
#    )
#    
#    helpdesk_email = schema.EMail(
#        title=u"Helpdesk E-mail",
#        description=u"Generic helpdesk email address of this provider; not specific to any service.",
#        required=False,
#    )

    directives.widget(supported_os=CheckBoxFieldWidget)
    supported_os = schema.List(
        title=u'Supported Operating Systems',
        value_type=schema.Choice(vocabulary='dpmt.operating_systems'),
        required=False,
        missing_value=[],
    )

    getAccount = schema.URI(
        title=u"Account",
        description=u"URL to instructions on how to get an account",
        required=False,
    )

    registry_link = schema.TextLine(title=u'Central Registry', readonly=True)
    directives.widget('registry_link', TrustedTextWidget)


@implementer(IProvider)
class Provider(Container, CommonUtilities):
    """Provider instance"""

    @property
    def link2offers(self):
        # Warning! In a property the obj self is not acquisition-wrapped.
        # So you don't have self.__parent__ or self.absolute_url() here!
        # To get the object you need to get it like this:
        wrapped = api.content.get(UID=self.UID())
        try:
            offers = wrapped['offers']
        except KeyError:
            return "No offers found"
        url = offers.absolute_url()
        title = u"Resources offered by {}".format(self.title)
        anchor = u"<a href='{}?unit=TiB' title='{}'>{}</a>".format(
            url, title, title)
        return anchor

    @property
    def registry_link(self):
        return self.getCregURL()
