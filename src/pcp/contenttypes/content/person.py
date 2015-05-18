"""Definition of the Person content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from pcp.contenttypes.interfaces import IPerson
from pcp.contenttypes.config import PROJECTNAME

PersonSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    ateapi.FormattableNameField('name',
        required=1,
        subfields=('firstnames', 'lastname'),
        subfield_labels={'firstnames':'First name(s)',
                         'lastname':'Last name(s)'},
    ),
    ateapi.EmailField('email'),
    atapi.ReferenceField('affiliation',
                         relationship='affiliated',
                         allowed_types=('Center', 'Community'),
                         ),
    ateapi.PhoneNumbersField('phone'),    
))


schemata.finalizeATCTSchema(
    PersonSchema,
    folderish=True,
    moveDiscussion=False
)


class Person(folder.ATFolder):
    """A person involved in a project."""
    implements(IPerson)

    meta_type = "Person"
    schema = PersonSchema


atapi.registerType(Person, PROJECTNAME)
