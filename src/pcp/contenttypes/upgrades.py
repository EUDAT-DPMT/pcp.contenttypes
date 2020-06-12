# -*- coding: UTF-8 -*-
from plone import api
from plone.app.contenttypes.migration.migration import migrateCustomAT
from plone.dexterity.interfaces import IDexterityFTI
from zope.globalrequest import getRequest

import logging

log = logging.getLogger(__name__)


def after_plone5_upgrade(context=None):
    """Various cleanup tasks after upgrade from Plone 4.3 to 5.2
    """
    # reinstall pcp.contenttypes to enable new dx types
    portal_setup - api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
        'profile-pcp.contenttypes:default', purge_old=False)
    remove_all_revisions()
    # workaround issue with versioning for now
    disable_versioning()


def install_pac(context=None):
    """Run this in Plone 5.2
    """
    portal = api.portal.get()
    request = getRequest()
    installer = api.content.get_view('installer', portal, request)
    installer.install_product('plone.app.contenttypes')


def migrate_folders(context=None):
    portal = api.portal.get()
    request = getRequest()
    pac_migration = api.content.get_view('migrate_from_atct', portal, request)
    content_types = ['Folder']
    pac_migration(
        migrate=True,
        content_types=content_types,
        migrate_schemaextended_content=True,
        migrate_references=False,
        reindex_catalog=False,
        patch_searchabletext=True,
    )


def migrate_to_dexterity(context=None):
    portal = api.portal.get()
    request = getRequest()
    pac_migration = api.content.get_view('migrate_from_atct', portal, request)
    content_types = [
        'Document',
        'Event',
        'File',
        'Image',
        'Link',
        'News Item',
        'Topic',
        'Collection',
        ]
    pac_migration(
        migrate=True,
        content_types=content_types,
        migrate_schemaextended_content=True,
        migrate_references=False,
        reindex_catalog=False,
        patch_searchabletext=True,
    )


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


def remove_all_revisions(context=None):
    """Remove all revisions.
    After packing the DB this could significantly shrink its size.
    """
    hs = api.portal.get_tool('portal_historiesstorage')
    zvcr = hs.zvc_repo
    zvcr._histories.clear()
    storage = hs._shadowStorage
    storage._storage.clear()


def disable_versioning(context=None):
    """disable_versioning for all DX types
    """
    portal_types = api.portal.get_tool('portal_types')
    versioning = 'plone.versioning'
    for fti in portal_types.listTypeInfo():
        if not IDexterityFTI.providedBy(fti) or versioning not in fti.behaviors:
            continue
        behaviors = list(fti.behaviors)
        behaviors.remove(versioning)
        behaviors = tuple(behaviors)
        fti._updateProperty('behaviors', behaviors)
        log.info(u'Disabled versioning for {}'.format(fti.id))
