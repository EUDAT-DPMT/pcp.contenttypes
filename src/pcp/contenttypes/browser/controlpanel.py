from plone.app.registry.browser import controlpanel

from pcp.contenttypes.interfaces.settings import ISettings


class SettingsEditForm(controlpanel.RegistryEditForm):

    schema = ISettings
    label = u'DPTMP settings'
    description = u''

    def updateFields(self):
        super(SettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(SettingsEditForm, self).updateWidgets()


class SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SettingsEditForm

