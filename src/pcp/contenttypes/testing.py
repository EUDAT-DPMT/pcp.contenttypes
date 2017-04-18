from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.testing import z2
from zope.configuration import xmlconfig


class PcpcontenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.ATExtensions
        import Products.ATBackRef
        import collective.handleclient
        import plone.formwidget.datetime
        import pcp.contenttypes
        import zopyx

        xmlconfig.file('configure.zcml', Products.ATExtensions, context=configurationContext)
        xmlconfig.file('configure.zcml', Products.ATBackRef,  context=configurationContext)
        xmlconfig.file('configure.zcml', collective.handleclient, context=configurationContext)
        xmlconfig.file('configure.zcml', plone.formwidget.datetime, context=configurationContext)
        xmlconfig.file('configure.zcml', pcp.contenttypes, context=configurationContext)
        xmlconfig.file('configure.zcml', zopyx.plone.persistentlogger, context=configurationContext)

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')
        z2.installProduct(app, 'Products.ATExtensions')
        z2.installProduct(app, 'pcp.contenttypes')

    def tearDownZope(self, app):
        # Uninstall products installed above
        # z2.uninstallProduct(app, 'Products.PloneFormGen')
        z2.uninstallProduct(app, 'Products.ATExtensions')
        z2.uninstallProduct(app, 'pcp.contenttypes')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.ATBackRef:default')
        applyProfile(portal, 'Products.ATExtensions:default')
        applyProfile(portal, 'collective.handleclient:default')
        applyProfile(portal, 'pcp.contenttypes:default')
        applyProfile(portal, 'plone.formwidget.datetime:default')
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
