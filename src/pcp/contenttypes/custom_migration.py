# -*- coding: UTF-8 -*-
from collective.relationhelpers import api as relapi
from plone import api
from plone.app.contenttypes.migration.migration import migrateCustomAT

import logging

log = logging.getLogger(__name__)

# Field Migrators

def migrate_adress(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate ateapi.AddressField to multiple dx fields
    """
    address = src_obj.address
    dst_obj.street1 = address.get('street1')
    dst_obj.street2 = address.get('street2')
    dst_obj.zip = address.get('zip')
    dst_obj.city = address.get('city')
    dst_obj.country = address.get('country')


# def compute_resources_migrator(src_obj, dst_obj, src_fieldname, dst_fieldname):
#     """Migrate ateapi.RecordsField compute_resources to datagrid
#     """
#     compute_resources = src_obj.compute_resources
#     dx_value = {}
#     for k, v in compute_resources.items():
#         setattr(dst_obj, k, v)


# def storage_resources_migrator(src_obj, dst_obj, src_fieldname, dst_fieldname):
#     """Migrate ateapi.RecordsField storage_resources to datagrid
#     """
#     storage_resources = src_obj.storage_resources
#     for k, v in storage_resources.items():
#         setattr(dst_obj, k, v)


def migrate_simple_datagrid(src_obj, dst_obj, src_fieldname, dst_fieldname):
    """Migrate RecordsField to datagrid if fields are exactly the same;
    Maybe there are problems with text/bytes?
    """
    at_values = src_obj.getField(src_fieldname).get(src_obj)
    dx_values = []
    for at_value in at_values:
        dx_value = {}
        for key, val in at_value.items():
            if isinstance(at_value, tuple):
                val = tuple(safe_unicode(i) for i in val)
            if isinstance(at_value, list):
                val = [safe_unicode(i) for i in val]
            dx_value[key] = val
        dx_values.append(dx_value)
    setattr(dst_obj, dst_fieldname, dx_values)


# Some AT fields have different names than the relationships!
FIELD_RELATIONSHIP_MAPPING = {
    'admins': 'community_admins',
}

def migrate_relations(src_obj, dst_obj, src_fieldname, dst_fieldname):
    src_fieldname = FIELD_RELATIONSHIP_MAPPING.get(src_fieldname, src_fieldname)
    reference_catalog = api.portal.get_tool('reference_catalog')
    if not reference_catalog:
        return
    # During migration the uid has already moved to dst_obj (=the dexterity target)!
    # That's why src_obj.getField(src_fieldname).get(src_obj) is empty!
    uid = dst_obj.UID()
    for brain in reference_catalog._optimizedQuery(uid=uid, indexname='sourceUID', relationship=src_fieldname):
        rel = brain.getObject()
        target = rel.getTargetObject()
        relapi.link_objects(dst_obj, target, relationship=dst_fieldname)


# Field mappings for behaviors to inject into content-type mappings
# CommonFields => IDPMTCommon
fields_mapping_common = [
        {'AT_field_name': 'identifiers',
         'DX_field_name': 'identifiers',
         'field_migrator': migrate_simple_datagrid,
         },
        {'AT_field_name': 'additional',
         'DX_field_name': 'additional',
         'field_migrator': migrate_simple_datagrid,
         },
    ]

# ConditionsFields => IDPMTConstraints
fields_mapping_constraints = [
        {'AT_field_name': 'regional_constraints',
         'DX_field_name': 'regional_constraints',
         },
        {'AT_field_name': 'thematic_constraints',
         'DX_field_name': 'thematic_constraints',
         },
        {'AT_field_name': 'organizational_constraints',
         'DX_field_name': 'organizational_constraints',
         },
        {'AT_field_name': 'constraints',
         'DX_field_name': 'constraints',
         'dx_fieldtype': 'RichText',
         },
    ]

# RequestFields => IDPMTRequest
fields_mapping_request = [
        {'AT_field_name': 'startDate',
         'DX_field_name': 'startDate',
         'dx_fieldtype': 'Datetime',
         },
        {'AT_field_name': 'endDate',
         'DX_field_name': 'endDate',
         'dx_fieldtype': 'Datetime',
         },
        {'AT_field_name': 'preferred_providers',
         'DX_field_name': 'preferred_providers',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'constraints',
         'DX_field_name': 'constraints',
         'dx_fieldtype': 'RichText',
         },
        {'AT_field_name': 'ticketid',
         'DX_field_name': 'ticketid',
         },
    ]

# ResourceFields => IDPMTResource
fields_mapping_resource = [
        {'AT_field_name': 'compute_resources',
         'DX_field_name': 'compute_resources',
         'field_migrator': migrate_simple_datagrid,
         },
        {'AT_field_name': 'storage_resources',
         'DX_field_name': 'storage_resources',
         'field_migrator': migrate_simple_datagrid,
         },
    ]

# ResourceContextFields => IDPMTResourceContext
fields_mapping_resourcecontext = [
        {'AT_field_name': 'project',
         'DX_field_name': 'project',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'customer',
         'DX_field_name': 'customer',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'contact',
         'DX_field_name': 'contact',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'request',
         'DX_field_name': 'request',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'services',
         'DX_field_name': 'services',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name': 'linked_resources',
         'DX_field_name': 'linked_resources',
         'field_migrator': migrate_relations,
         },
    ]


def migrate_community(context=None):
    fields_mapping = [
        {'AT_field_name': 'url',
         'DX_field_name': 'url',
         },
        {'AT_field_name': 'address',
         'DX_field_name': 'address',
         'field_migrator': migrate_adress,
         },
        {'AT_field_name':'VAT',
         'DX_field_name':'VAT',
         },
        {'AT_field_name':'representative',
         'DX_field_name':'representative',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name':'admins',
         'DX_field_name':'community_admins',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name':'topics',
         'DX_field_name':'topics',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Community',
        dst_type='community_dx')


def migrate_community(context=None):
    fields_mapping = [
        {'AT_field_name': 'url',
         'DX_field_name': 'url',
         },
        {'AT_field_name': 'address',
         'DX_field_name': 'address',
         'field_migrator': migrate_adress,
         },
        {'AT_field_name':'VAT',
         'DX_field_name':'VAT',
         },
        {'AT_field_name':'representative',
         'DX_field_name':'representative',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name':'admins',
         'DX_field_name':'community_admins',
         'field_migrator': migrate_relations,
         },
        {'AT_field_name':'topics',
         'DX_field_name':'topics',
         },
    ]
    fields_mapping += fields_mapping_common
    migrateCustomAT(
        fields_mapping,
        src_type='Community',
        dst_type='community_dx')
