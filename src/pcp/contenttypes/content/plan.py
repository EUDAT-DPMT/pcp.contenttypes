"""Definition of the Plan content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IPlan
from pcp.contenttypes.config import PROJECTNAME

PlanSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(PlanSchema, moveDiscussion=False)


class Plan(base.ATCTContent):
    """The Master Plan for a community"""
    implements(IPlan)

    meta_type = "Plan"
    schema = PlanSchema


atapi.registerType(Plan, PROJECTNAME)
