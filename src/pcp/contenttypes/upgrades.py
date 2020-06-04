# -*- coding: UTF-8 -*-
from plone.app.contenttypes.migration.migration import migrateCustomAT


def test_at_migration(context=None):
    migrate_service()

def migrate_service():
    fields_mapping = (
            {'AT_field_name': 'description_internal',
             'DX_field_name': 'description_internal',
             },
    )
    migrateCustomAT(
        fields_mapping,
        src_type='Service',
        dst_type='service_dx')