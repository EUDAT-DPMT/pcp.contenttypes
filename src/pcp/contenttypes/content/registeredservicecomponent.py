"""Definition of the RegisteredServiceComponent content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from pcp.contenttypes.interfaces import IRegisteredServiceComponent
from pcp.contenttypes.config import PROJECTNAME

RegisteredServiceComponentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))


schemata.finalizeATCTSchema(RegisteredServiceComponentSchema, moveDiscussion=False)


class RegisteredServiceComponent(base.ATCTContent):
    """A CDI admin registers a new service component"""
    implements(IRegisteredServiceComponent)

    meta_type = "RegisteredServiceComponent"
    schema = RegisteredServiceComponentSchema

    atapi.ReferenceField('service_providers',
                         read_permission='View internals',
                         write_permission='Modify internals',
                         relationship='provided_by',
                         allowed_types=('Provider',),
                         multiValued=True,
                         widget=ReferenceBrowserWidget(label='Service provider(s)',
                                                       description='The provider(s) hosting this service component.',
                                                       allow_browse=1,
                                                       startup_directory='/providers',
                                                      ),
                         ),


atapi.registerType(RegisteredServiceComponent, PROJECTNAME)
