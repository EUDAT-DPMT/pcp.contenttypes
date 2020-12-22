# -*- coding: UTF-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IFieldWidget
from z3c.form.browser.text import TextWidget
from z3c.form.interfaces import ITextWidget
from z3c.form.widget import FieldWidget
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.intid.interfaces import IIntIds
from zope.schema import TextLine
from zope.schema._bootstrapfields import TextLine
from zope.schema.interfaces import IField
from zope.schema.interfaces import ITextLine


class IBackrelField(ITextLine):

    relation = TextLine(
        title=u'Relation',
        description=u'The relation to display',
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
                u'BackrelField requires a relation, e.g. relation="relatedItems"'
            )
        super(BackrelField, self).__init__(required=False, **kw)


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
        results = []
        inaccessible_results = []
        if IAddForm.providedBy(self.form):
            return results
        from_attribute = self.field.relation
        relation_catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        intid = intids.getId(self.context)
        query = {'to_id': intid}
        if from_attribute != 'all_relations':
            query['from_attribute'] = from_attribute

        sm = getSecurityManager()
        checkPermission = getSecurityManager().checkPermission
        for rel in relation_catalog.findRelations(query):
            obj = rel.from_object
            if checkPermission('View', obj):
                results.append(obj)
        return IContentListing(results)


@adapter(IBackrelField, IPloneFormLayer)
@implementer(IFieldWidget)
def BackrelFieldWidget(field, request):
    return FieldWidget(field, BackrelWidget(request))
