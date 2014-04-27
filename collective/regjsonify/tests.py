# -*- coding: utf-8 -*-

import unittest
from collective.regjsonify.interfaces import IJSONifier
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.registry.fieldfactory import persistentFieldAdapter
from plone.registry.fieldfactory import choicePersistentFieldAdapter
from zope import interface
from zope import schema
from zope.component import queryUtility
from zope.component import provideAdapter, testing


class ITest(interface.Interface):
    
    simple_text = schema.TextLine(title=u"Simple Text",
                                  default=u"Lorem Ipsum")


class RegJSONifyTestCase(unittest.TestCase):
    
    def setUp(self):
        provideAdapter(persistentFieldAdapter)
        provideAdapter(choicePersistentFieldAdapter)
        self.registry = Registry()
        self.registry.registerInterface(ITest)
        self.proxy = self.registry.forInterface(ITest)

    def tearDown(self):
        testing.tearDown(self)
    
    def test_textline(self):
       data = IJSONifier(self.proxy)
       # todo