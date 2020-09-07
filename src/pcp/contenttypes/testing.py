from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2


class PcpcontenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # import collective.handleclient
        import zopyx
        import pcp.contenttypes
        import collective.z3cform.datagridfield
        # self.loadZCML(package=collective.handleclient)
        self.loadZCML(package=zopyx.plone.persistentlogger)
        self.loadZCML(package=collective.z3cform.datagridfield)
        self.loadZCML(package=pcp.contenttypes)

    def tearDownZope(self, app):
        pass
        # Uninstall products installed above

    def setUpPloneSite(self, portal):
        # applyProfile(portal, 'collective.handleclient:default')
        applyProfile(portal, 'collective.z3cform.datagridfield:default')
        applyProfile(portal, 'pcp.contenttypes:default')
        applyProfile(portal, 'zopyx.plone.persistentlogger:default')

PCP_CONTENTTYPES_FIXTURE = PcpcontenttypesLayer()
PCP_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PCP_CONTENTTYPES_FIXTURE,),
    name="PcpcontenttypesLayer:Integration"
)
PCP_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PCP_CONTENTTYPES_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PcpcontenttypesLayer:Functional"
)
