# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from renocopro.policy.testing import RENOCOPRO_POLICY_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


no_get_installer = False


try:
    from Products.CMFPlone.utils import get_installer
except Exception:
    no_get_installer = True


class TestSetup(unittest.TestCase):
    """Test that renocopro.policy is properly installed."""

    layer = RENOCOPRO_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if renocopro.policy is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'renocopro.policy'))

    def test_browserlayer(self):
        """Test that IRenocoproPolicyLayer is registered."""
        from renocopro.policy.interfaces import (
            IRenocoproPolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRenocoproPolicyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RENOCOPRO_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('renocopro.policy')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if renocopro.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'renocopro.policy'))

    def test_browserlayer_removed(self):
        """Test that IRenocoproPolicyLayer is removed."""
        from renocopro.policy.interfaces import \
            IRenocoproPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IRenocoproPolicyLayer,
            utils.registered_layers())
