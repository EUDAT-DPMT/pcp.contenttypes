# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.folder.interfaces import IOrdering
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from zExceptions import BadRequest
from zope.interface import alsoProvides

import logging


log = logging.getLogger(__name__)


def cleanup(context=None):
    portal = api.portal.get()
    app = portal.__parent__
    if 'demo' in app.keys():
        app.manage_delObjects(['demo'])

    # remove openid plugin
    acl = api.portal.get_tool('acl_users')
    try:
        acl.manage_delObjects(['openid'])
        log.info('Deleted openid plugin')
    except BadRequest:
        pass


def fix_some_at_folders(context=None):
    # fix some AT objects
    portal = api.portal.get()

    def treeify(obj, path):
        if getattr(obj, 'portal_type', None) in ['RegisteredServiceComponent', 'RegisteredService']:
            if not obj._tree:
                alsoProvides(obj, IOrdering)
                BTreeFolder2Base._initBTrees(obj)
                log.info(u'Fix _tree for {}'.format(obj))

    portal.ZopeFindAndApply(portal, search_sub=True, apply_func=treeify)


def prepare_plone5_upgrade(context=None):
    remove_overrides()
    release_all_webdav_locks()
    remove_all_revisions()
    disable_theme()
    remove_ploneformgen()
    catalog = api.portal.get_tool('portal_catalog')
    qi = api.portal.get_tool('portal_quickinstaller')
    portal_setup = api.portal.get_tool('portal_setup')

    to_delete = [
        '/pcp/enabling',
        '/pcp/projects/proj-elte/elte-request',
    ]
    for path in to_delete:
        try:
            obj = api.content.get(path=path)
            if obj is not None:
                api.content.delete(obj, check_linkintegrity=False)
                log.info('Deleted %s' % path)
        except:  # noqa: F401
            continue

    addons = [
        'Products.Poi',
        'uwosh.pfg.d2c',
        'Poi',
        'collective.js.jqueryui',
        'zopyx.plone.cassandra',
        'DataGridField',
        'collective.contentstats',
        'AutoUserMakerPASPlugin',
    ]
    for addon in addons:
        if qi.isProductInstalled(addon):
            log.info(u'Uninstalling {}'.format(addon))
            qi.uninstallProducts([addon])
        else:
            log.info(u'{} is not installed'.format(addon))
    rebuild_catalog()
    pack_database()


def remove_ploneformgen(context=None):
    portal = api.portal.get()
    portal_types = api.portal.get_tool('portal_types')
    portal_catalog = api.portal.get_tool('portal_catalog')
    qi = api.portal.get_tool('portal_quickinstaller')

    log.info('removing PloneFormGen')
    old_types = [
        'FormFolder',
    ]
    old_types = [i for i in old_types if i in portal_types]
    for old_type in old_types:
        for brain in portal_catalog(portal_type=old_type):
            log.info(u'Deleting Existing Instances of {}!'.format(old_type))
            api.content.delete(brain.getObject(), check_linkintegrity=True)
    try:
        portal.manage_delObjects(['formgen_tool'])
    except AttributeError:
        pass
    try:
        portal.portal_properties.manage_delObjects(['ploneformgen_properties'])
    except BadRequest:
        pass

    if qi.isProductInstalled('PloneFormGen'):
        qi.uninstallProducts(['PloneFormGen'])

    if qi.isProductInstalled('Products.PloneFormGen'):
        qi.uninstallProducts(['Products.PloneFormGen'])


def remove_overrides(context=None):
    # TODO: Move all skin stuff into this package!!!!!

    # log.info('removing portal_skins overrides')
    # portal_skins = api.portal.get_tool('portal_skins')
    # custom = portal_skins['custom']
    # for name in custom.keys():
    #     custom.manage_delObjects([name])
    #     log.info(u'Removed skin item {}'.format(name))

    log.info('removing portal_view_customizations')
    view_customizations = api.portal.get_tool('portal_view_customizations')
    for name in view_customizations.keys():
        view_customizations.manage_delObjects([name])
        log.info(u'Removed portal_view_customizations item {}'.format(name))


def release_all_webdav_locks(context=None):
    from Products.CMFPlone.utils import base_hasattr

    portal = api.portal.get()

    def unlock(obj, path):
        if base_hasattr(obj, 'wl_isLocked') and obj.wl_isLocked():
            obj.wl_clearLocks()
            log.info(u'Unlocked {}'.format(path))

    portal.ZopeFindAndApply(portal, search_sub=True, apply_func=unlock)


def remove_all_revisions(context=None):
    """Remove all revisions.
    After packing the DB this could significantly shrink its size.
    """
    hs = api.portal.get_tool('portal_historiesstorage')
    zvcr = hs.zvc_repo
    zvcr._histories.clear()
    storage = hs._shadowStorage
    storage._storage.clear()


def disable_theme(context=None):
    """Disable a custom diazo theme and enable sunburst.
    Useful for cleaning up a site in Plone 4
    """
    theme_name = 'plonetheme.onegov'
    from plone.app.theming.utils import applyTheme

    portal_skins = api.portal.get_tool('portal_skins')
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(theme_name):
        log.info('Uninstalling {}'.format(theme_name))
        qi.uninstallProducts([theme_name])
    log.info('Disabling all diazo themes')
    try:
        applyTheme(None)
    except AttributeError:
        pass
    log.info('Enabled Sunburst Theme')
    portal_skins.default_skin = 'Sunburst Theme'
    if theme_name in portal_skins.getSkinSelections():
        portal_skins.manage_skinLayers([theme_name], del_skin=True)


def cleanup_in_plone52(context=None):
    from plone.app.upgrade.utils import cleanUpSkinsTool
    portal = api.portal.get()
    cleanUpSkinsTool(portal)
    portal_properties = api.portal.get_tool('portal_properties')
    portal_properties.manage_delObjects(['quickupload_properties'])
    portal_properties.manage_delObjects(['imaging_properties'])
    pack_database()


def pack_database(context=None):
    """Pack the database"""
    portal = api.portal.get()
    app = portal.__parent__
    db = app._p_jar.db()
    db.pack(days=0)


def rebuild_catalog(context=None):
    log.info('rebuilding catalog')
    catalog = api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
