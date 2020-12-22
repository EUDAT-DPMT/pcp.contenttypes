# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from pcp.contenttypes.content_dx.accountable import Accountable
from pcp.contenttypes.content_dx.common import CommonUtilities
from pcp.contenttypes.content_dx.accountable import IAccountable
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class ISize(Interface):

    value = schema.TextLine(
        title=u'Value',
        required=False,
    )

    unit = schema.Choice(
        title=u'Unit',
        vocabulary='dpmt.information_units',
        required=False,
    )

    storage_class = schema.Choice(
        title=u'Storage class',
        vocabulary='dpmt.storage_types',
        required=False,
    )


class IRegisteredStorageResource(model.Schema):
    """Dexterity Schema for Registered Storage Resources"""

    size = schema.List(
        title=u'Size',
        description=u'Maximal size and type of this storage resource',
        value_type=DictRow(title=u'Foo', schema=ISize),
        default=[{'value': None, 'unit': None, 'storage_class': None}],
        required=False,
    )
    directives.widget(
        'size',
        DataGridFieldFactory,
        auto_append=False,
        allow_insert=False,
    )

    usage = schema.TextLine(title=u'Current usage', readonly=True)

    number = schema.TextLine(title=u'Registered objects', readonly=True)

    allocated = schema.TextLine(title=u'Allocated storage', readonly=True)

    storage_class = schema.TextLine(title=u'Storage class', readonly=True)

    max_objects = schema.Int(
        title=u"Max. Objects",
        description=u"Allocated (maximum) number of objects",
        required=False,
    )

    cost_factor = schema.Float(
        title=u"Cost factor",
        required=False,
    )

    preserve_until = schema.Datetime(
        title=u"Preserve until",
        description=u"Until when does this resource need to be allocated?",
        required=False,
    )
    directives.widget('preserve_until', DatetimeFieldWidget)


@implementer(IRegisteredStorageResource)
@implementer(IAccountable)
class RegisteredStorageResource(Container, CommonUtilities, Accountable):
    """RegisteredStorageResource instance"""

    @property
    def usage(self):
        return self.renderMemoryValue(
            self.getUsedMemory() and self.getUsedMemory()['core']
        )

    @property
    def number(self):
        return self.getNumberOfRegisteredObjects()

    @property
    def allocated(self):
        return self.renderMemoryValue(self.getAllocatedMemory())

    @property
    def storage_class(self):
        return self.size and self.size[0]['storage_class']

    def getCachedRecords(self):
        return getattr(self, 'cached_records', None)

    def getUsedMemory(self):
        return getattr(self, 'cached_newest_record', None)

    def getAllocatedMemory(self):
        size = self.size[0]
        if size.get('value') and size.get('unit'):
            # unit should be enforced by field's vocabulary
            try:
                float(size['value'])
            except ValueError:
                return None
            return size
        else:
            return None

    def getResourceUsage(self):
        used = self.getUsedMemory()
        size = self.getAllocatedMemory()

        if used:
            meta = used['meta']
            submission_time = meta['submission_time']
        else:
            submission_time = '??'

        return '%s (%s UTC)' % (
            self.renderResourceUsage(used and used['core'], size),
            submission_time,
        )

    def getNumberOfRegisteredObjects(self, as_int=False):
        used = self.getUsedMemory()
        number = None
        if used:
            number = used['meta'].get('number', None)
        if as_int:
            if number in [None, '']:
                return 0
            else:
                return int(number)
        return number

    def getScopeValues(self, asString=0):
        """Return the human readable values of the scope keys"""
        project = self.project
        if project is None:
            if asString:
                return ''
            else:
                return ('',)
        scopes = []
        scopes.extend(project.getScopeValues())
        s = set(scopes)
        if asString:
            return ", ".join(s)
        return s  # tuple(s)
