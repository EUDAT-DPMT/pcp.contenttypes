"""Definition of the Plan content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IPlan
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities

PlanSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.ReferenceField('principle_investigator',
                         relationship='principal_investigator',
                         allowed_types=('Person',),
                         widget=ReferenceBrowserWidget(label='Principal investigator',
                                                       allow_browse=1,
                                                       startup_directory='/people',
                                                       ),
                         ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(PlanSchema, moveDiscussion=False)


class Plan(base.ATCTContent, CommonUtilities):
    """The Master Plan for a community"""
    implements(IPlan)

    meta_type = "Plan"
    schema = PlanSchema


atapi.registerType(Plan, PROJECTNAME)
