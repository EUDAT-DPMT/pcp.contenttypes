"""Common components shared by content types
"""

from Products.Archetypes import atapi
from Products.ATExtensions import ateapi

CommonFields = atapi.Schema((
    atapi.ComputedField('uid',
                        expression="here.UID()",
                        ),
    ateapi.RecordsField('identifiers',
                        searchable=0,  # RR: we should probably provide an index method
                        required=0,
                        subfields = ('type', 'value'),
                        subfield_labels ={'type':'Identifier'},
                        subfield_vocabularies = {'type':'identifierTypes'},
                        innerJoin = ': ',
                        outerJoin = '<br />',
                        widget=ateapi.RecordsWidget(
                            description = "Other identifiers used to refer "\
                            "to this information.",
                            label = u"Identifiers",
                            ),
    ),
    ateapi.RecordsField('additional',
                        subfields = ('key', 'value'),
                        minimalSize=3,
                        subfield_sizes={'key': 15,
                                        },
                        innerJoin = ': ',
                        outerJoin = '<br />',
                        widget=ateapi.RecordsWidget(
                            description="Other key-value pairs to characterise "\
                            "this item. Use this specifically to signal information "\
                            "that you think should be included in the fields above."
                            ),
                        ),
    atapi.TextField('text',
                    required=False,
                    searchable=True,
                    primary=True,
                    storage=atapi.AnnotationStorage(migrate=True),
                    validators=('isTidyHtmlWithCleanup',),
                    default_output_type='text/x-html-safe',
                    widget=atapi.RichWidget(
                        description=u'Any other additional information not '\
                        'covered so far.',
                        label=u'Text',
                        rows=15,
                        ),
    ),
))


class CommonUtilities(object):
    """Mixin class to provide shared functionality across content types"""

    def identifierTypes(self, instance):
        """Controlled vocabulary for the supported PID systems"""

        return ateapi.getDisplayList(instance, 'identifier_types', add_select=True)

        
