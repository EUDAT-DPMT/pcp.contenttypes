from pcp.contenttypes.testing import PCP_CONTENTTYPES_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestExample(unittest.TestCase):

    layer = PCP_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if dynajet.site is installed."""
        self.assertTrue(self.installer.is_product_installed('pcp.contenttypes'))

    def test_browserlayer(self):
        """Test that IDynajetSiteLayer is registered."""
        from pcp.contenttypes.interfaces import IPcpContenttypesLayer
        from plone.browserlayer import utils

        self.assertIn(IPcpContenttypesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PCP_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('pcp.contenttypes')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if dynajet.site is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed('dynajet.site'))
