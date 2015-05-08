from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class PcpcontenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import pcp.contenttypes
        xmlconfig.file(
            'configure.zcml',
            pcp.contenttypes,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pcp.contenttypes:default')

PCP_CONTENTTYPES_FIXTURE = PcpcontenttypesLayer()
PCP_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PCP_CONTENTTYPES_FIXTURE,),
    name="PcpcontenttypesLayer:Integration"
)
PCP_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PCP_CONTENTTYPES_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PcpcontenttypesLayer:Functional"
)
