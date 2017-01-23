# patches to by applied using collective.monkeypatcher
# follows advice from
# http://docs.plone.org/develop/plone/misc/monkeypatch.html


#
# patch the diff tool to support some of ATEXtensions' fields
# (record(s) in particular) in diff view
#

from Products.CMFDiffTool.TextDiff import TextDiff
from Products.CMFDiffTool.TextDiff import AsTextDiff
from Products.CMFDiffTool.FieldDiff import FieldDiff
from Products.CMFDiffTool.BinaryDiff import BinaryDiff
from Products.CMFDiffTool.ListDiff import ListDiff

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


#################################################################################################
# $HOME/.buildout/eggs/plone.app.workflow-2.1.9-py2.7.egg/plone/app/workflow/browser/sharing.py
#################################################################################################

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

        old_ac_local_roles_block = getattr(self.context, '__ac_local_roles_block__', None)

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
            old_userids = set([tp[0] for tp in old_settings if list(tp[1]) != ['Owner']])
            new_userids = set([d['id'] for d in settings if d['roles']])
            all_userids = old_userids | new_userids
            removed_userids = old_userids - new_userids
            added_userids = new_userids - old_userids

#            print old_userids
#            print new_userids
#            print removed_userids
#            print added_userids
#
#            import pprint
#            pprint.pprint(settings)
            reindex = self.update_role_settings(settings, reindex=False) \
                        or reindex
        if reindex:
            self.context.reindexObjectSecurity()
            notify(LocalrolesModifiedEvent(self.context, self.request))


        new_ac_local_roles_block = getattr(self.context, '__ac_local_roles_block__', None)

        print old_ac_local_roles_block
        print new_ac_local_roles_block


        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."), type='info')

    # Other buttons return to the sharing page
    if cancel_button:
        postback = False

    return postback

from plone.app.workflow.browser.sharing import SharingView
SharingView.handle_form = sharing_handle_form

