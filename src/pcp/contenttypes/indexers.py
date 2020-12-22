from collective.dexteritytextindexer.converters import DefaultDexterityTextIndexFieldConverter
from collective.dexteritytextindexer.interfaces import IDexterityTextIndexFieldConverter
from plone.dexterity.interfaces import IDexterityContent
from z3c.form.interfaces import IWidget
from z3c.relationfield.interfaces import IRelationChoice
from z3c.relationfield.interfaces import IRelationList
from zope.component import adapter
from zope.interface import implementer


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IRelationChoice, IWidget)
class RelationChoiceFieldConverter(DefaultDexterityTextIndexFieldConverter):
    """Converts the data of a relationchoice field"""

    def convert(self):
        """return the title of the relation item."""
        storage = self.field.interface(self.context)
        if self.field.get(storage):
            relation = self.field.get(storage)
            return relation.to_object.title


@implementer(IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IRelationList, IWidget)
class RelationListFieldConverter(DefaultDexterityTextIndexFieldConverter):

    def convert(self):
        """return the title of the relation item."""
        result = []
        storage = self.field.interface(self.context)
        if self.field.get(storage):
            for relation in self.field.get(storage):
                result.append(relation.to_object.title)
        return ' '.join(result)
