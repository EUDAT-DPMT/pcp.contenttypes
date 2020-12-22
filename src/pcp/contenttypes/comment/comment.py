from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IWidget
from z3c.form.widget import FieldWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.interface import implementer
from zope.schema import Field
from zope.schema import TextLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import ITextLine


class ICommentField(ITextLine):

    comment = TextLine(
        title='Comment',
        description='The comment to display',
        required=False,
    )


@implementer(ICommentField, IFromUnicode)
class CommentField(Field):
    """A field that stores nothing but displays a comment defined in the schema."""

    def __init__(self, **kw):
        self.comment = kw.pop('comment', '')
        if not self.comment:
            raise ValueError('CommentField requires a comment, e.g. comment="Foo"')
        super().__init__(required=False, **kw)


class ICommentWidget(IWidget):
    """Comment Widget Interface"""


@implementer(ICommentWidget)
class CommentWidget(Widget):
    """Widget for CommentField"""


@adapter(ICommentField, IPloneFormLayer)
@implementer(IFieldWidget)
def CommentFieldWidget(field, request):
    return FieldWidget(field, CommentWidget(request))
