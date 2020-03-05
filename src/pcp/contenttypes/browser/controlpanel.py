# -*- coding: UTF-8 -*-
from pcp.contenttypes.interfaces.settings import ISettings
from plone.app.registry.browser import controlpanel


class SettingsEditForm(controlpanel.RegistryEditForm):

    schema = ISettings
    schema_prefix = 'dpmt'
    label = u'DPTMP settings'
    description = u''


class SettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SettingsEditForm
