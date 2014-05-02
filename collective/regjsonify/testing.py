# -*- coding: utf-8 -*-

from plone.testing import z2
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.configuration import xmlconfig
from zope.component import provideAdapter


class RegJSONifyLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.regjsonify
        xmlconfig.file('configure.zcml',
                       collective.regjsonify,
                       context=configurationContext)
        z2.installProduct(app, 'collective.regjsonify')


REG_JSONIFY_FIXTURE = RegJSONifyLayer()
REG_JSONIFY_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(REG_JSONIFY_FIXTURE, ),
                       name="RegJSONify:Integration")
REG_JSONIFY_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(REG_JSONIFY_FIXTURE, ),
                       name="RegJSONify:Functional")
