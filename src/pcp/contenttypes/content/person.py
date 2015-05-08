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
    ateapi.AddressField('address',
                        searchable=1,
                        subfields=('street1', 'street2', 'zip',
                                   'city', 'state', 'country'),
                        ),
    ateapi.LabeledUrlField('affiliation',
             #FIXME: This should be updated, so we can use target="_blank" in html
             required=True,
             searchable=1,
             default={},
             subfield_labels={'label':'Name'},
             subfield_maxlength={'label':120,
                                 'url':120,
                                 },
             widget=ateapi.LabeledUrlWidget(description="Institutional affiliation, e.g. an "
                                                        "institute or department at a university or "
                                                        "a company.",
                                            ),
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
