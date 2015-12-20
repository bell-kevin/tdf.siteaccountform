# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tdf.siteaccountform


class TdfSiteaccountformLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=tdf.siteaccountform)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tdf.siteaccountform:default')


TDF_SITEACCOUNTFORM_FIXTURE = TdfSiteaccountformLayer()


TDF_SITEACCOUNTFORM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TDF_SITEACCOUNTFORM_FIXTURE,),
    name='TdfSiteaccountformLayer:IntegrationTesting'
)


TDF_SITEACCOUNTFORM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TDF_SITEACCOUNTFORM_FIXTURE,),
    name='TdfSiteaccountformLayer:FunctionalTesting'
)


TDF_SITEACCOUNTFORM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TDF_SITEACCOUNTFORM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='TdfSiteaccountformLayer:AcceptanceTesting'
)
