# -*- coding: UTF-8 -*-
from Acquisition import aq_base
from collective.relationhelpers import api as relapi
from ComputedAttribute import ComputedAttribute
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.interfaces import IDexterityFTI
from plone.folder.interfaces import IOrdering
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.CMFPlone.utils import get_installer
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

import logging
import os
import six
import transaction

log = logging.getLogger(__name__)
RELATIONS_KEY = 'ALL_REFERENCES'


def after_plone5_upgrade(context=None):
    """Various cleanup tasks after upgrade from Plone 4.3 to 5.2
    """
    # reinstall pcp.contenttypes to enable new dx types
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    portal_setup = api.portal.get_tool('portal_setup')
    portal_setup.runAllImportStepsFromProfile(
        'profile-pcp.contenttypes:default', purge_old=False)

    loadMigrationProfile(
        context,
        'profile-Products.CMFPlone:plone',
        steps=['controlpanel'],
    )

    cleanup_skins()
    remove_broken_steps()
    remove_all_revisions()
    # workaround issue with versioning for now
    disable_versioning()
    rebuild_catalog()
    pack_database()


def store_references(context=None):
    from plone.app.contenttypes.migration.utils import store_references
    portal = api.portal.get()
    store_references(portal)
    relapi.purge_relations()
    relapi.cleanup_intids()


def install_pac(context=None):
    """Run this in Plone 5.2
    """
    portal = api.portal.get()
    request = getRequest()
    installer = api.content.get_view('installer', portal, request)
    installer.install_product('plone.app.contenttypes')


def migrate_folders(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
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
    rebuild_catalog()


def migrate_to_dexterity(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    portal = api.portal.get()
    request = getRequest()
    pac_migration = api.content.get_view('migrate_from_atct', portal, request)
    content_types = 'all'
    pac_migration(
        migrate=True,
        content_types=content_types,
        migrate_schemaextended_content=True,
        migrate_references=False,
        reindex_catalog=False,
        patch_searchabletext=True,
    )
    loadMigrationProfile(
        context,
        'profile-pcp.contenttypes:default',
        steps=['workflow', 'typeinfo'],
    )
    disable_versioning()  # because it was re-enabled by typeinfo
    rebuild_catalog()


def custom_at_migration(context=None):
    # Disable queueing of indexing/reindexing/unindexing
    queue_indexing = os.environ.get('CATALOG_OPTIMIZATION_DISABLED', None)
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    obsolete = [
        'Plan',
        'Service Details',
        'Resource',
    ]
    for portal_type in obsolete:
        for brain in api.content.find(portal_type=portal_type):
            obj = brain.getObject()
            log.info(u'Remove {} at {}'.format(portal_type, obj.absolute_url()))
            api.content.delete(obj, check_linkintegrity=False)

    from pcp.contenttypes import custom_migration
    custom_migration.migrate_project()
    custom_migration.migrate_community()
    custom_migration.migrate_downtime()
    custom_migration.migrate_environment()
    custom_migration.migrate_person()
    custom_migration.migrate_provider()
    custom_migration.migrate_registeredcomputeresource()
    custom_migration.migrate_registeredresource()
    custom_migration.migrate_registeredservice()
    custom_migration.migrate_registeredservicecomponent()
    custom_migration.migrate_registeredstorageresource()
    custom_migration.migrate_resourceoffer()
    custom_migration.migrate_resourcerequest()
    custom_migration.migrate_service()
    custom_migration.migrate_servicecomponent()
    custom_migration.migrate_servicecomponentimplementation()
    custom_migration.migrate_servicecomponentimplementationdetails()
    custom_migration.migrate_servicecomponentoffer()
    custom_migration.migrate_servicecomponentrequest()
    custom_migration.migrate_serviceoffer()
    custom_migration.migrate_servicerequest()
    if queue_indexing:
        os.environ['CATALOG_OPTIMIZATION_DISABLED'] = queue_indexing
    else:
        del os.environ['CATALOG_OPTIMIZATION_DISABLED']
    rebuild_catalog()


# Map some AT Reference to DX Relation
RELATIONSHIP_FIELD_MAPPING = {
    # old AT Relations!
    'relatesTo': 'relatedItems',
    'done_for': 'community',
    'using': 'registered_services_used',
    'enabled_by': 'project_enabler',
    'admin_of': 'admins',
    'managers_for': 'managers',
    'implemented_by': 'service_component_implementation_details',
    'provided_by': 'service_providers',
    'contact_for': 'contacts',
    'rolerequest_for_context': 'context',
    'owned_by': 'service_owner',
    'slas_offered': 'slas',
    'affiliated': 'affiliation',
    'depends_on': 'dependencies',
    'service_option_offered': 'service_option',
    # These fields were renamed in DX to match the relations:
    # 'service_offered': 'service',
    # 'community_admins': 'admins',
    # 'service_component_offered': 'service_component',
    # 'service_component_implementations_offered': 'implementations',
    # 'requested_component': 'service_component',
    # 'requested_component_implementations': 'implementations',
}


def get_from_attribute(rel):
    source_obj = uuidToObject(rel['from_uuid'])
    if source_obj.portal_type == 'serviceoffer_dx' and rel['relationship'] == 'contact_for':
        return 'contact'
    if source_obj.portal_type == 'registeredservice_dx' and rel['relationship'] == 'contact_for':
        return 'contact'
    if source_obj.portal_type == 'environment_dx' and rel['relationship'] == 'contact_for':
        return 'contact'
    # normal mapping
    return RELATIONSHIP_FIELD_MAPPING.get(
        rel['relationship'], rel['relationship'])



def restore_references(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    portal = api.portal.get()
    all_stored_relations = IAnnotations(portal)[RELATIONS_KEY]
    log.info('Loaded {0} relations to restore'.format(
        len(all_stored_relations))
    )
    all_fixed_relations = []
    # pac exports references with 'relationship' relapi expects 'from_attribute'
    # also some fields have special relationship-names in AT
    for rel in all_stored_relations:
        if not uuidToObject(rel['from_uuid']):
            continue
        if not uuidToObject(rel['to_uuid']):
            continue
        # drop outdated relations
        if rel['relationship'] in ['primary_provider_for', 'secondary_provider_for']:
            continue
        rel['from_attribute'] = get_from_attribute(rel)
        all_fixed_relations.append(rel)
    relapi.restore_relations(all_relations=all_fixed_relations)
    rebuild_catalog()


def remove_archetypes(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    portal_types = api.portal.get_tool('portal_types')
    portal_catalog = api.portal.get_tool('portal_catalog')
    to_drop = [
        'Plan',
        'Resource',
        'Service Details',
        'AliasVocabulary',
        'SimpleVocabulary',
        'SimpleVocabularyTerm',
        'SortedSimpleVocabulary',
        'TreeVocabulary',
        'TreeVocabularyTerm',
        'VdexFileVocabulary',
        ]
    for portal_type in to_drop:
        for brain in portal_catalog(portal_type=portal_type):
            obj = brain.getObject()
            log.info(u'Removing {} at {}'.format(portal_type, brain.getURL()))
            api.content.delete(obj=obj, check_linkintegrity=False)
    KEEP = [
        'Plone Site',
        'Comment',
        'TempFolder',
        'Discussion Item',
        'VocabularyLibrary',
        ]
    from plone.dexterity.interfaces import IDexterityFTI
    for fti in portal_types.listTypeInfo():
        if IDexterityFTI.providedBy(fti) or fti.id in KEEP:
            continue
        brains = portal_catalog(portal_type=fti.id)
        if brains:
            log.info(u'{} existing Instances of Type {}!'.format(len(brains), fti.id))
        else:
            portal_types.manage_delObjects([fti.id])
            log.info(u'Removed Type {}!'.format(fti.id))

    portal = api.portal.get()
    old_installer = api.portal.get_tool('portal_quickinstaller')
    old_installer.uninstallProducts(['ATBackRef'])
    old_installer.uninstallProducts(['ATExtensions'])

    new_installer = get_installer(portal)
    # uninstall AT Types and some dependency tools
    new_installer.uninstall_product('Products.ATContentTypes')

    old_installer.uninstallProducts(['ATVocabularyManager'])

    # uninstall AT
    new_installer.uninstall_product('Archetypes')

    # remove obsolete AT tools
    tools = [
        'portal_languages',
        'portal_tinymce',
        'kupu_library_tool',
        'portal_factory',
        'portal_atct',
        'uid_catalog',
        'archetype_tool',
        'reference_catalog',
        'portal_metadata',
        'portal_vocabularies',
    ]
    for tool in tools:
        if tool not in portal.keys():
            log.info('Tool {} not found'.format(tool))
            continue
        try:
            portal.manage_delObjects([tool])
            log.info('Deleted {}'.format(tool))
        except Exception as e:
            log.info(u'Problem removing {}: {}'.format(tool, e))
            try:
                log.info(u'Fallback to remove without permission_checks')
                portal._delObject(tool)
                log.info('Deleted {}'.format(tool))
            except Exception as e:
                log.info(u'Another problem removing {}: {}'.format(tool, e))

    pprops = api.portal.get_tool('portal_properties')
    if 'extensions_properties' in pprops:
        pprops.manage_delObjects('extensions_properties')


def rebuild_relations(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    disable_versioning()
    remove_all_revisions()
    relapi.rebuild_relations()


def fix_stuff(context=None):
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    if 'plone.app.controlpanel.wicked' in annotations:
        del annotations['plone.app.controlpanel.wicked']

    # Fix conversations that still have the old AT co tehnt as __parent__
    # TODO: Fix in plone.app.contenttypes?
    def fix_at_remains(obj, path):
        annotations = getattr(aq_base(obj), '__annotations__', None)
        if not annotations:
            return
        if 'plone.app.discussion:conversation' not in annotations.keys():
            return
        conversation = annotations['plone.app.discussion:conversation']
        if 'broken' in conversation.__parent__.__repr__():
            conversation.__parent__ = obj
            log.info(u'Fix conversation for {}'.format(obj.absolute_url()))
        else:
            log.info(u'Conversation parent ok: {}'.format(conversation.__parent__))
    portal.ZopeFindAndApply(portal, search_sub=True, apply_func=fix_at_remains)

    # remove openid plugin
    acl = api.portal.get_tool('acl_users')
    try:
        acl.manage_delObjects(['openid'])
        log.info('Deleted openid plugin')
    except BadRequest:
        pass


def remove_broken_registry_entries(context=None):
    records = [
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_core',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_widget',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_mouse',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_position',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_draggable',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_droppable',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_resizable',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_selectable',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_sortable',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_accordion',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_autocomplete',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_button',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_datepicker',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_dialog',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_menu',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_progressbar',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_slider',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_spinner',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_tabs',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_tooltip',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_blind',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_bounce',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_clip',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_drop',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_explode',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_fade',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_fold',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_highlight',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_pulsate',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_scale',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_shake',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_slide',
        'collective.js.jqueryui.controlpanel.IJQueryUIPlugins.ui_effect_transfer',
        'collective.js.jqueryui.controlpanel.IJQueryUICSS.css',
        'collective.js.jqueryui.controlpanel.IJQueryUICSS.patch',
        'Products.ResourceRegistries.interfaces.settings.IResourceRegistriesSettings.resourceBundlesForThemes',
        'plone.resourceBundlesForThemes',
    ]
    registry = getUtility(IRegistry)
    for record in records:
        try:
            del registry.records[record]
            log.info('Removed record {}'.format(record))
        except KeyError:
            pass


def remove_utilities(context=None):
    """Example that removes collective.zipfiletransport
    """
    portal = api.portal.get()
    sm = portal.getSiteManager()

    from Products.CMFCore.interfaces import IMetadataTool
    if IMetadataTool in sm.utilities._adapters[0]:
        del sm.utilities._adapters[0][IMetadataTool]
        log.info(u'Unregistering adapter for MetadataTool')

    if IMetadataTool in sm.utilities._subscribers[0]:
        del sm.utilities._subscribers[0][IMetadataTool]
        log.info(u'Unregistering subscriber for MetadataTool')

    if IMetadataTool in sm.utilities._provided:
        del sm.utilities._provided[IMetadataTool]
        log.info(u'Unregistering subscriber for MetadataTool')

    if (IMetadataTool, '') in sm._utility_registrations:
        del sm._utility_registrations[(IMetadataTool, '')]
        log.info(u'Drop subscriber for MetadataTool')

    from Products.CMFCore.interfaces import IDiscussionTool
    for util in sm.getAllUtilitiesRegisteredFor(IDiscussionTool):
        sm.unregisterUtility(util, IDiscussionTool)
        log.info(u'Removed IDiscussionTool utility')

    sm.utilities._p_changed = True
    transaction.commit()


def cleanup_after_py3_migration(context=None):
    if not six.PY3:
        raise RuntimeError('This needs top run in Python 3!')
    fix_portlets()


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


def rebuild_catalog(context=None):
    log.info('rebuilding catalog')
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()


def pack_database(context=None):
    """Pack the database"""
    portal = api.portal.get()
    app = portal.__parent__
    db = app._p_jar.db()
    db.pack(days=0)


def cleanup_skins(context=None):
    to_delete = [
        'referencebrowser',
        'favicon.ico',
        'logo.png',
        'maintenance_icon.png',
        'detailed_view',
        'hasJSON',
        'len',
        'shibboleth',
        'demo_method',
        'fgvalidate_base',
        'getServices',
        'initialzeAccount',
        'kss_generic_macros',
        'manage_raiseRequest',
        'migrateOffers',
        'backreferencewidget',
        'trusted_string',
        ]
    portal_skins = api.portal.get_tool('portal_skins')
    custom = portal_skins.custom
    for item in to_delete:
        if item in custom:
            custom.manage_delObjects(item)
            log.info(u'Removed {} from portal_skins/custom.'.format(item))


def remove_broken_steps(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    broken_import_steps = [
        'collective.z3cform.datetimewidget',
        'languagetool',
        'ploneformgen',
        'uwosh.pfg.d2c.install',
        'zopyx.plone.cassandra.various',
        'various-atextensions',
    ]
    log.info('remove import-steps')
    registry = portal_setup.getImportStepRegistry()
    for broken_import_step in broken_import_steps:
        if broken_import_step in registry.listSteps():
            registry.unregisterStep(broken_import_step)

    broken_export_steps = [
        'languagetool',
    ]
    log.info('remove export-steps')
    registry = portal_setup.getExportStepRegistry()
    for broken_export_step in broken_export_steps:
        if broken_export_step in registry.listSteps():
            registry.unregisterStep(broken_export_step)
    portal_setup._p_changed = True


def fix_portlets(context=None):
    """Fix portlets that use ComputedValue for path-storage instead of a UUID.
    """
    os.environ['CATALOG_OPTIMIZATION_DISABLED'] = '1'
    catalog = api.portal.get_tool('portal_catalog')
    portal = api.portal.get()
    fix_portlets_for(portal)
    for brain in catalog.getAllBrains():
        try:
            obj = brain.getObject()
        except KeyError:
            log.info('Broken brain for {}'.format(brain.getPath()))
            continue
        fix_portlets_for(obj)


def fix_portlets_for(obj):
    """Fix portlets for a certain object."""
    attrs_to_fix = [
        'root_uid',
        'search_base_uid',
        'uid',
    ]
    if getattr(obj.aq_base, 'getLayout', None) is not None and obj.getLayout() is not None:
        try:
            view = obj.restrictedTraverse(obj.getLayout())
        except KeyError:
            view = obj.restrictedTraverse('@@view')
    else:
        view = obj.restrictedTraverse('@@view')
    for manager_name in ['plone.leftcolumn', 'plone.rightcolumn', 'plone.footerportlets']:
        manager = queryUtility(IPortletManager, name=manager_name, context=obj)
        if not manager:
            continue
        mappings = queryMultiAdapter((obj, manager), IPortletAssignmentMapping)
        if not mappings:
            continue
        for key, assignment in mappings.items():
            for attr in attrs_to_fix:
                if getattr(assignment, attr, None) is not None and isinstance(getattr(assignment, attr), ComputedAttribute):
                    setattr(assignment, attr, None)
                    log.info('Reset {} for portlet {} assigned at {} in {}'.format(attr, key, obj.absolute_url(), manager_name))  # noqa: E501
                    log.info('You may need to configure it manually at {}/@@manage-portlets'.format(obj.absolute_url()))  # noqa: E501


def fix_recent_portlet(context=None):
    from plone.portlets.constants import CONTENT_TYPE_CATEGORY
    from plone.portlets.constants import CONTEXT_CATEGORY
    from plone.portlets.constants import GROUP_CATEGORY
    from plone.portlets.constants import USER_CATEGORY
    from zope.component import getUtilitiesFor
    from plone.portlets.interfaces import IPortletManager
    from zope.container import contained
    portal = api.portal.get()
    fixing_up = contained.fixing_up
    contained.fixing_up = True

    # find assignments in the global categories
    for category in (USER_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY):
        for manager_name, manager in getUtilitiesFor(IPortletManager):
            for key, mapping in manager.get(category, {}).items():
                mapping = mapping.__of__(portal)
                for key in mapping:
                    if 'recent-items' in key or 'calendar' in key:
                        del mapping[key]
                        log.info(u'removed recent items portlet from {}'.format(manager_name))
    contained.fixing_up = fixing_up
    loadMigrationProfile(
        context,
        'profile-pcp.contenttypes:default',
        steps=['portlets'],
    )
