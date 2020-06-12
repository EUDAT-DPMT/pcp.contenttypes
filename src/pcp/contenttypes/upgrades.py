# -*- coding: UTF-8 -*-
from plone.app.contenttypes.migration.migration import migrateCustomAT
#from plone import api
#import logging
#log = logging.getLogger(__name__)

def test_at_migration(context=None):
    migrate_service()

def migrate_service():
    fields_mapping = (
            {'AT_field_name': 'description_internal',
             'DX_field_name': 'description_internal',
             },
            {'AT_field_name': 'url',
             'DX_field_name': 'url',
             },             
            {'AT_field_name':'service_area',
             'DX_field_name':'service_area',
             },
    )
    #service_at = api.content.get(path='/catalog/B2DROP')
    #log.info(service_at.__dict__)
    #import pdb; pdb.set_trace()
    migrateCustomAT(
        fields_mapping,
        src_type='Service',
        dst_type='service_dx')
    #service_dx = api.content.get(path='/catalog/B2DROP')
    #log.info(service_dx.__dict__)
    #import pdb; pdb.set_trace()
