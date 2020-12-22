from collective.relationhelpers import api as relapi
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.schema import TextLine
from zope.schema.interfaces import ITextLine


class IBackrelField(ITextLine):

    relation = TextLine(
        title='Relation',
        description='The relation to display',
        required=False,
    )


@implementer(IBackrelField)
class BackrelField(TextLine):
    """A field that stores nothing but points to a relation to display.

    In Add-Forms it shows nothing. In Edit and View it shows the relations
    as links the same way as RelationChoice and RelationList fields do.
    """

    def __init__(self, **kw):
        self.relation = kw.pop('relation', '')
        if not self.relation:
            raise ValueError(
                'BackrelField requires a relation, e.g. relation="relatedItems"'
            )
        super().__init__(required=False, **kw)


class IBackrelWidget(ITextWidget):
    """Backrel Widget Interface"""


@implementer(IBackrelWidget)
class BackrelWidget(TextWidget):
    """Widget for BackrelField"""

    def items(self):
        """Return items for the relation specified in the field.

        Check view-permission to only display items that the user is allowed to see.
        Uses IContentListing for easy access to MimeTypeIcon and more.
        The template is the same as for RelationChoice and RelationList.
        """
        if IAddForm.providedBy(self.form):
            return []
        relations = relapi.backrelations(self.context, self.field.relation)
        if relations:
            return IContentListing(relations)


@adapter(IBackrelField, IPloneFormLayer)
@implementer(IFieldWidget)
def BackrelFieldWidget(field, request):
    return FieldWidget(field, BackrelWidget(request))
