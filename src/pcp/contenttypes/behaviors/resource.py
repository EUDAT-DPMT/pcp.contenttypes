"""Resource behaviours for DPMT content types.

Includes form fields and behaviour adapters for specifying
resource amounts
"""
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


# parts for the data grid type fields
class IComputeResourceRowSchema(Interface):

    nCores = schema.TextLine(
        title='Number of cores',
        required=False,
    )

    ram = schema.TextLine(
        title='RAM',
        required=False,
    )

    diskspace = schema.TextLine(
        title='Diskspace',
        required=False,
    )

    system = schema.TextLine(
        title='requires OS/software',
        required=False,
    )

    virtualization = schema.Choice(
        title='Virtualization OK?',
        values=['Yes', 'No'],
        required=False,
    )


class IStorageResourceRowSchema(Interface):

    value = schema.TextLine(
        title='Value',
        required=False,
    )

    unit = schema.Choice(
        title='Unit',
        vocabulary='dpmt.information_units',
        required=False,
    )

    storage_class = schema.Choice(
        title='Storage class',
        vocabulary='dpmt.storage_types',
        required=False,
    )


@provider(IFormFieldProvider)
class IDPMTResource(model.Schema):
    """Add fields to specify resource amounts"""

    fieldset(
        'resources',
        label='Resources',
        fields=('compute_resources', 'storage_resources'),
    )

    compute_resources = schema.List(
        title='Compute resources',
        description='Specification of the compute resources',
        value_type=DictRow(
            title='Compute resources', schema=IComputeResourceRowSchema
        ),
        required=False,
        missing_value=[],
    )
    directives.widget('compute_resources', DataGridFieldFactory)

    storage_resources = schema.List(
        title='Storage resources',
        description='Specification of the storage resources',
        value_type=DictRow(
            title='Storage resources', schema=IStorageResourceRowSchema
        ),
        required=False,
        missing_value=[],
    )
    directives.widget('storage_resources', DataGridFieldFactory)
