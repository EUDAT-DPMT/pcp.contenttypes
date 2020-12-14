# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.schema.email import Email
from plone.supermodel import model
from z3c.form.interfaces import IDisplayForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IPhone(Interface):
    """Schema for Datagrid field phone
    """
    number_type = schema.Choice(
        title=u'Type',
        values=[
            u'Office',
            u'Secretariat',
            u'Laboratory',
            u'Mobile',
            u'Fax',
            u'Private',
            ],
        required=False,
        )

    number = schema.TextLine(
        title=u'Number',
        required=False,
        )


class IPerson(model.Schema):
    """Dexterity Schema for Persons
    """
    dexteritytextindexer.searchable('email')

    name = schema.TextLine(title=u'Name', readonly=True)

    directives.omitted(IDisplayForm, 'firstname', 'lastname')
    firstname = schema.TextLine(title=u'First name(s)')

    lastname = schema.TextLine(title=u'Last name(s)')

    email = Email(
        title=u"E-mail",
        required=False,
    )

    affiliation = RelationChoice(
        title=u"Affiliation",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "affiliation",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["provider_dx","community_dx"],
            "basePath": make_relation_root_path,
        },
    )

    phone = schema.List(
        title=u"Phone",
        value_type=DictRow(schema=IPhone),
        required=False,
        missing_value=[],
    )
    directives.widget('phone', DataGridFieldFactory)

    manages = BackrelField(
        title=u'Managed by',
        relation='managed_by',
        )

    provider_contact_for = BackrelField(
        title=u'General contact for',
        relation='contact',
        )

    business_contact_for = BackrelField(
        title=u'Business contact for',
        relation='business_contact',
        )

    security_contact_for = BackrelField(
        title=u'Security contact for',
        relation='security_contact',
        )

    provider_admin = BackrelField(
        title=u'Administrator for',
        relation='admins',
        )

    she_contact = BackrelField(
        title=u'SHE contact for',
        relation='contact_for',
        )

    community_contact_for = BackrelField(
        title=u'Customer contact for',
        relation='community_contact',
        )

    community_representative = BackrelField(
        title=u'Customer representative for',
        relation='representative',
        )

    community_admin = BackrelField(
        title=u'Customer administrator for',
        relation='community_admins',
        )

    enables = BackrelField(
        title=u'Project enabler for',
        relation='project_enabler',
        )

    service_owner_of = BackrelField(
        title=u'Service owner of',
        relation='service_owner',
        )

    principal_investigator_of = BackrelField(
        title=u'Principal investigator of',
        relation='principal_investigator',
        )

    manager_of_registered_service = BackrelField(
        title=u'Manager of registered services',
        relation='managers',
        )

@implementer(IPerson)
class Person(Container):
    """Person instance"""

    @property
    def name(self):
        return u'{} {}'.format(self.firstname, self.lastname)
