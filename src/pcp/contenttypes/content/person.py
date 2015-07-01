"""Definition of the Person content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from Products.ATBackRef import BackReferenceField
from Products.ATBackRef import BackReferenceWidget

from pcp.contenttypes.interfaces import IPerson
from pcp.contenttypes.config import PROJECTNAME
from pcp.contenttypes.content.common import CommonFields
from pcp.contenttypes.content.common import CommonUtilities


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
                         allowed_types=('Provider', 'Community'),
                         ),
    ateapi.PhoneNumbersField('phone'),
    BackReferenceField('manages',
                       relationship='managed_by',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('community_admins',
                       relationship='community_admins',
                       multiValued=True,
                       widget=BackReferenceWidget(label="Community administrator for",
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('community_representative',
                       relationship='representative',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Community representative for',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('community_contact_for',
                       relationship='community_contact',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Community contact for',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('enables',
                       relationship='enabled_by',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Project enabler for',
                                                  visible={'edit':'invisible'},
                                                  ),
                       ),
)) + CommonFields.copy()


schemata.finalizeATCTSchema(
    PersonSchema,
    folderish=True,
    moveDiscussion=False
)


class Person(folder.ATFolder, CommonUtilities):
    """A person involved in a project."""
    implements(IPerson)

    meta_type = "Person"
    schema = PersonSchema


atapi.registerType(Person, PROJECTNAME)
