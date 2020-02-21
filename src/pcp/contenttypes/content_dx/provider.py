# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class IProvider(model.Schema):
    """Dexterity Schema for Providers
    """

    dexteritytextindexer.searchable(
        'url',        
        'provider_type',
        'provider_status',
        'status_details',
        'infrastructure',
        'domain',
        'VAT',
        'emergency_phone',
        'alarm_email',
        'helpdesk_email',
        'supported_os'
    )

    url = schema.URI(
            title=u'Url',
            required=False,
            )

    #Computed field 'link2offers'

    provider_type = schema.TextLine(
            title=u'Provider type',
            required=False,
            )

    provider_userid = schema.TextLine(
            title=u'Provider user ID',
            required=True,
            )

    provider_status = schema.TextLine(
            title=u'Provider status',
            required=False,
            )

    status_details = schema.TextLine(
            title=u'Status details/comment',
            required=False,
            )

    infrastructure = schema.TextLine(
            title=u'Infrastructure',
            required=False,
            )

    domain = schema.TextLine(
            title=u'Domain',
            required=False,
            )

    #Address field

    VAT = schema.TextLine(
            title=u'VAT',
            required=False,
            )

    timezone = schema.TextLine(
            title=u'Time zone',
            required=False,
            )

    latitude = schema.TextLine(
            title=u'Latitude',
            description=u'If known; GOCDB can use this. (-90 <= number <= 90)',
            required=False,
            )

    longitude = schema.TextLine(
            title=u'Longitude',
            description=u'If known; GOCDB can use this. (-180 <= number <= 180)',
            required=False,
            )

    ip4range = schema.TextLine(
            title=u'IPv4 range',
            description=u'(a.b.c.d/e.f.g.h)',
            required=False,
            )

    ip6range = schema.TextLine(
            title=u'IPv6 range',
            required=False,
            )

    contact = RelationChoice(
            title=u'Contact',
            description=u'Main contact person for the operations of this provider.',
            source=CatalogSource(portal_type=['Person']),
            required=False,
            )

    business_contact = RelationChoice(
            title=u'Business contact',
            description=u'Main contact person for the financial matters of this provider.',
            source=CatalogSource(portal_type=['Person']),
            required=False,
            )

    security_contact = RelationChoice(
            title=u'Security contact',
            description=u'Person specifically to be contacted for security-related matters.',
            source=CatalogSource(portal_type=['Person']),
            required=False,
           )

   # to be implemented later 
   # admins = RelationList(
   #         title=u'Administrators',
   #         source=CatalogSource(portal_type=['Person']),
   #         )


    emergency_phone = schema.TextLine(
            title=u'Emergency telephone number',
            description=u'Include international prefix and area code',
            required=False,
            )
#alarm email
#helpdesk email
#supported os

    getAccount = schema.URI(
            title=u'Account',
            description=u'URL to instructions on how to get an account',
            required=False,
            )
#computedfield registry_link

@implementer(IProvider)
class Provider(Container):
    """Provider instance"""