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
                         allowed_types=('Center', 'Community'),
                         ),
    ateapi.PhoneNumbersField('phone'),
    BackReferenceField('manages',
                       relationship='managed_by',
                       multiValued=True,
                       widget=BackReferenceWidget(visible={'edit':'invisible'},
                                                  ),
                       ),
    BackReferenceField('community_contact_for',
                       relationship='community_contact',
                       multiValued=True,
                       widget=BackReferenceWidget(label='Community contact for',
                                                  description="The person from the community side responsible for this.",
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
    atapi.TextField('text',
                    primary=True,
                    widget=atapi.RichWidget(),
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
