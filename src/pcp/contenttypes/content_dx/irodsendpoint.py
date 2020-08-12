# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.relationhelpers import api as relapi
from pcp.contenttypes.backrels.backrelfield import BackrelField
from plone import api
from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.textfield import RichText
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IIrodsEndpoint(model.Schema):
    """Dexterity Schema for Irods endpoint
    """

    host = schema.TextLine(
            title=u'Host',
            required=False,
            )

    ip = schema.TextLine(
            title=u'IP',
            required=False,
            )

    zone_name = schema.TextLine(
            title=u'Zone name',
            required=False,
            )

    zone_key = schema.TextLine(
            title=u'Zone key',
            required=False,
      )

    monitored = schema.TextLine(
            title=u'Monitored?',
            description=u'Yes or no ',
            required=True,
            )

    monitoring_user = schema.TextLine(
            title=u'Monitoring user',
            required=False,
            )

    system_operations_user = schema.TextLine(
            title=u'Sytem operations user',
            required=False,
            )

    remote_user = schema.TextLine(
            title=u'Remote user names',
            description=u'Comma separated list of remote user names to be used.',
            required=False,
            )

    primary_path = schema.TextLine(
            title=u'Path',
            required=False,
            )
    
    path_description = schema.TextLine(
            title = u'Path description',
            required = False,
            )
    
    alternative_path = schema.TextLine(
            title=u'Alternative path',
            required=False,
            )
    
    alt_path_description = schema.TextLine(
            title=u'Alternative path description',
            required=False,
            )
    
    contacts = schema.TextLine(
        title=u'Contacts',
        required=False,
        )


    #<field name="related_project" type="plone.app.relationfield.Relation">
    #    <title>Related project</title>
    #    <required>False</required>
    #    <source>pcp.contenttypes.project_source</source>
    #</field>
    related_project = RelationChoice(
        title=u"Related project",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "related_project",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["project_dx"],
            "basePath": make_relation_root_path,
        },
    )

    #<field name="related_service" type="plone.app.relationfield.Relation">
    #    <title>Related service</title>
    #    <source>pcp.contenttypes.rs_source</source>
    #</field>
    related_service = RelationChoice(
        title=u"Related service",
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        "related_service",
        RelatedItemsFieldWidget,
        pattern_options={
            "selectableTypes": ["registeredservice_dx"],
            "basePath": make_relation_root_path,
        },
    )

    text = RichText(
        title=u'Text',
        description=u'Anything else to further describe this endpoint.',
        required=False
    )


@implementer(IIrodsEndpoint)
class IrodsEndpoint(Container):
    """IrodsEndpoint instance"""

#    @property
#    def registry_link(self):
#        return self.getCregURL()
#
#    @property
#    def scopes(self):
#        return self.getScopeValues(asString=True)
#
#    def getScopeValues(self, asString=False):
#        """Return the human readable values of the scope keys"""
#        projects = relapi.get_backrelations(self, 'registered_services_used', fullobj=True)
#        scopes = []
#        [scopes.extend(p['fullobj'].getScopeValues()) for p in projects]
#        s = set(scopes)
#        if asString:
#            return u', '.join(s)
#        return s  # tuple(s)
