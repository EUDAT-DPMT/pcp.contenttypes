# -*- coding: UTF-8 -*-
from collective import dexteritytextindexer
from plone.app.vocabularies.catalog import CatalogSource
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer

class IProject(model.Schema):
    """Dexterity Schema for Projects
    """

    website = schema.URI(
                title=u'Website',
                required=False,
                )

    #Reference field 'community'
    #Reference field 'community_contact'
    #Reference field 'registered_services_used'
    #Computed field 'allocated_new'
    #Computed field 'used_new'
    #Reference field 'general_provider'
    #Reference field 'project_enabler'

    start_date = schema.Datetime(
            title=u'Start date',
            required=False,
            )

    end_date = schema.Datetime(
            title=u'End date',
            required=False,
            )

    call_for_collaboration = schema.URI(
            title=u'Call for collaboration',
            description=u'URL to the call that triggered this project',
            required=False,
            )

    uptake_plan = schema.URI(
            title=u'Uptake plan',
            description=u'URL to the project uptake plan (if not available on this site). Otherwise, often found on the confluence site.',
            required=False,
            )

    repository = schema.TextLine(
            title=u'Repository',
            description=u'If the data to be dealt with here are in a web-accessible repository already you should specify its URL here.',
            required=False,
            )

    topics = schema.TextLine(
            title=u'Topics',
            description=u'Please mention the scientific field(s) the data originate from.',
            required=False,
            )

    #Can a LinesField in an Archetype type be transfered into a List in a Dexterity type?
    #scopes = schema.List(
    #        title=u'Scope',
    #        description=u'Tick all that apply. If in doubt, select "EUDAT".',
    #        required=True,
    #        )

    #Back reference field "resources"
    #Computed field "resource usage"
    #Computed field "registered objects"

@implementer(IProject)
class Project(Container):
    """Project instance"""


