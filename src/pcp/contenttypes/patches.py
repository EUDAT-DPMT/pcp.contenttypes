# patches to by applied using collective.monkeypatcher
# follows advice from
# http://docs.plone.org/develop/plone/misc/monkeypatch.html


#
# patch the diff tool to support some of ATEXtensions' fields
# (record(s) in particular) in diff view
#
import pcp
from Products.CMFDiffTool.TextDiff import TextDiff
from Products.CMFDiffTool.TextDiff import AsTextDiff
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.BinaryDiff import BinaryDiff
from Products.CMFDiffTool.ListDiff import ListDiff
from six.moves import map

NEW_AT_FIELD_MAPPING = {'text': 'variable_text',
                        'string': 'variable_text',
                        'datetime': FieldDiff,
                        'file': 'variable_binary',
                        'blob': 'variable_binary',
                        'image': BinaryDiff,
                        'lines': ListDiff,
                        'integer': FieldDiff,
                        'float': FieldDiff,
                        'fixedpoint': FieldDiff,
                        'boolean': FieldDiff,
                        'record': AsTextDiff,
                        'address': AsTextDiff,
                        'records': AsTextDiff,
                        'url': 'variable_text',
                        'reference': 'raw:ListDiff'}

# Now we have a callable method!
patched_field_mapping = lambda: NEW_AT_FIELD_MAPPING


def apply_patched_mapping(scope, original, replacement):
    setattr(scope, original, replacement())
    return


##########################################################################
# $HOME/.buildout/eggs/plone.app.workflow-2.1.9-py2.7.egg/plone/app/workflow/browser/sharing.py
##########################################################################

import plone.api
from plone.app.workflow.events import LocalrolesModifiedEvent
from plone.app.workflow import PloneMessageFactory as _
from Products.statusmessages.interfaces import IStatusMessage
from zope.event import notify


def sharing_handle_form(self):
    """
    We split this out so we can reuse this for ajax.
    Will return a boolean if it was a post or not
    """

    postback = True

    form = self.request.form
    submitted = form.get('form.submitted', False)
    save_button = form.get('form.button.Save', None) is not None
    cancel_button = form.get('form.button.Cancel', None) is not None
    if submitted and save_button and not cancel_button:
        if not self.request.get('REQUEST_METHOD', 'GET') == 'POST':
            raise Forbidden

        old_ac_local_roles_block = getattr(
            self.context, '__ac_local_roles_block__', None)

        authenticator = self.context.restrictedTraverse('@@authenticator',
                                                        None)
        if not authenticator.verify():
            raise Forbidden

        # Update the acquire-roles setting
        if self.can_edit_inherit():
            inherit = bool(form.get('inherit', False))
            reindex = self.update_inherit(inherit, reindex=False)
        else:
            reindex = False

        entries = form.get('entries', [])
        roles = [r['id'] for r in self.roles()]
        settings = []
        for entry in entries:
            settings.append(
                dict(id=entry['id'],
                     type=entry['type'],
                     roles=[r for r in roles
                            if entry.get('role_%s' % r, False)]))
        if settings:

            old_settings = self.context.get_local_roles()
            old_settings_dict = dict([(userid, set(roles))
                                      for userid, roles in old_settings])
            settings_dict = dict([(d['id'], set(d['roles']))
                                  for d in settings])

            old_userids = set(
                [tp[0] for tp in old_settings if list(tp[1]) != ['Owner']])
            new_userids = set([d['id'] for d in settings if d['roles']])
            all_userids = old_userids | new_userids

            reindex = self.update_role_settings(settings, reindex=False) \
                or reindex
            new_ac_local_roles_block = getattr(
                self.context, '__ac_local_roles_block__', None)

            diff_context = dict()
            diff_context['removed_userids'] = old_userids - new_userids
            diff_context['added_userids'] = new_userids - old_userids
            diff_context['block_localroles'] = bool(new_ac_local_roles_block)
            diff_context['role_changes'] = dict()
            for userid, roles in settings_dict.items():
                old_roles = old_settings_dict.get(userid, set())
                if roles == old_roles:
                    continue

                roles_added = roles - old_roles
                roles_removed = old_roles - roles
                user = plone.api.user.get(userid)
                fullname = email = None
                if user:
                    fullname = user.getProperty('fullname')
                    email = user.getProperty('email')
                diff_context['role_changes'][userid] = dict(
                    fullname=fullname, email=email, added=roles_added, removed=roles_removed)

        if reindex:
            self.context.reindexObjectSecurity()
            event = LocalrolesModifiedEvent(self.context, self.request)
            event.diff_context = diff_context
            notify(event)

        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."), type='info')

    # Other buttons return to the sharing page
    if cancel_button:
        postback = False

    return postback

from plone.app.workflow.browser.sharing import SharingView
SharingView.handle_form = sharing_handle_form


from Products.PluggableAuthService.plugins.exportimport import getPackagePath
try:
    from Products.GenericSetup.utils import PageTemplateResource
except ImportError: # BBB
    from Products.PageTemplates.PageTemplateFile \
        import PageTemplateFile as PageTemplateResource


def export(self, export_context, subdir, root=False):
    """ See IFilesystemExporter.
    """
    info = self._getExportInfo()

    def update_user(user):
        # extend user dict by email and fullname
        memberdata = plone.api.user.get(userid=user['user_id'])
        if memberdata:
            email = memberdata.getProperty('email')
            fullname = memberdata.getProperty('fullname')
        else:
            email = ''
            fullname = ''
        user.update(email=email, fullname=fullname)
        return user

    def update_role(role):
        # wrap principal id in dict and extend user information
        principals = [dict(user_id=principal_id) for principal_id in role['principals']]
        role['principals'] = list(map(update_user, principals))
        return role

    if self._FILENAME == 'zodbusers.xml':
        # override source_users.xml with version containing fullname and email
        template = PageTemplateResource('overrides/%s' % self._FILENAME,
                                        pcp.contenttypes.__path__[0]).__of__(self.context)
        info['users'] = list(map(update_user, info['users']))
    elif self._FILENAME == 'zodbroles.xml':
        # override portal_role_manager.xml with version containing fullname and email
        template = PageTemplateResource('overrides/%s' % self._FILENAME,
                                        pcp.contenttypes.__path__[0]).__of__(self.context)
        info['roles'] = list(map(update_role, info['roles']))
    else:
        package_path = getPackagePath(self)
        template = PageTemplateResource('xml/%s' % self._FILENAME,
                                        package_path).__of__(self.context)

    export_context.writeDataFile('%s.xml' % self.context.getId(),
                                 template(info=info).encode('utf-8'),
                                 'text/xml',
                                 subdir,
                                 )

from Products.PluggableAuthService.plugins.exportimport import SimpleXMLExportImport
SimpleXMLExportImport.export = export
