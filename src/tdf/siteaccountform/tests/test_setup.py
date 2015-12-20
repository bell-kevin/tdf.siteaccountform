# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from tdf.siteaccountform.testing import TDF_SITEACCOUNTFORM_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that tdf.siteaccountform is properly installed."""

    layer = TDF_SITEACCOUNTFORM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tdf.siteaccountform is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tdf.siteaccountform'))

    def test_browserlayer(self):
        """Test that ITdfSiteaccountformLayer is registered."""
        from tdf.siteaccountform.interfaces import (
            ITdfSiteaccountformLayer)
        from plone.browserlayer import utils
        self.assertIn(ITdfSiteaccountformLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TDF_SITEACCOUNTFORM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['tdf.siteaccountform'])

    def test_product_uninstalled(self):
        """Test if tdf.siteaccountform is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tdf.siteaccountform'))

    def test_browserlayer_removed(self):
        """Test that ITdfSiteaccountformLayer is removed."""
        from tdf.siteaccountform.interfaces import ITdfSiteaccountformLayer
        from plone.browserlayer import utils
        self.assertNotIn(ITdfSiteaccountformLayer, utils.registered_layers())
