# -*- coding: UTF-8 -*-
from collective.relationhelpers import api as relapi
from plone import api
from plone.app.contenttypes.migration.migration import migrateCustomAT

import logging

log = logging.getLogger(__name__)


def migrate_community(context=None):
    fields_mapping = (
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
    )
    migrateCustomAT(
        fields_mapping,
        src_type='Community',
        dst_type='community_dx')


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
