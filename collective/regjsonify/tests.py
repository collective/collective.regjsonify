# -*- coding: utf-8 -*-

import unittest
from collective.regjsonify.interfaces import IJSONifier
from collective.regjsonify.interfaces import IJSONFieldDumper
from collective.regjsonify.fields import Base as JSONifyBase
from collective.regjsonify.testing import REG_JSONIFY_INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from plone.registry import Registry
from plone.registry.field import PersistentField
from plone.registry.fieldfactory import persistentFieldAdapter
from plone.registry.fieldfactory import choicePersistentFieldAdapter
from z3c.form.object import registerFactoryAdapter
from zope import interface
from zope import schema
from zope.component import queryUtility
from zope.component import getGlobalSiteManager
from zope.component import testing
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


test_vocab = SimpleVocabulary((
   SimpleTerm(value=1, token='sunny', title=u'Sunny'),
   SimpleTerm(value=2, token='raining', title=u'Raining')))


class ITestPersistentObject(interface.Interface):
    pass

class TestPersistentObject(PersistentField, schema.Object):
    interface.implements(ITestPersistentObject)


class IUnknown(interface.Interface):
    data_1 = schema.TextLine(title=u"Some text", default=u"Foo bar")
    data_2 = schema.TextLine(title=u"Other text", default=u"Baz qux")

class Unknown(object):
    interface.implements(IUnknown)
    
    def __init__(self):
        self.data_1 = u'a'
        self.data_2 = u'b'

registerFactoryAdapter(IUnknown, Unknown)


class UnknownField(JSONifyBase):
    
    def data(self, record):
        return {'data_1': record.data_1,
                'data_2': record.data_2}


class ITest(interface.Interface):
    
    simple_text = schema.TextLine(title=u"Simple Text", default=u"Lorem Ipsum")
    long_text = schema.Text(title=u"Long Text", default=u"Lorem Ipsum")
    ascii = schema.ASCIILine(title=u"ASCII", default="1234-abc")
    number1 = schema.Int(title=u"An int", default=24)
    number2 = schema.Float(title=u"An float", default=11.2)
    tf = schema.Bool(title=u"True or False", default=True)
    list_of = schema.List(title=u"A list",
                          value_type=schema.TextLine(),
                          default=['aaa', 'bbb'])
    tuple_of = schema.Tuple(title=u"A tuple",
                            value_type=schema.TextLine(),
                            default=('aaa', 'bbb'))
    choose = schema.Choice(title=u"Choose",
                           values=[1,2,3],
                           default=1,
                           )
    multiple_choice = schema.Tuple(title=u"Multiple choice",
                                   default=(1, 3),
                                   value_type=schema.Choice(values=(1, 2, 3, 4))
                                   )
    unknown_type = schema.Tuple(title=u"A set of unknown",
                               value_type=TestPersistentObject(IUnknown,
                                                               title=u"A persistent something"),
                               default=(Unknown(), ),
                               missing_value=())


class RegJSONifyTestCase(unittest.TestCase):
    
    layer = REG_JSONIFY_INTEGRATION_TESTING
    
    def setUp(self):
        super(RegJSONifyTestCase, self).setUp()
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(UnknownField, (ITestPersistentObject,), provided=IJSONFieldDumper)
        self.registry = Registry()
        self.registry.registerInterface(ITest)
        self.proxy = self.registry.forInterface(ITest)

    def test_textline(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('simple_text' in data.json().keys())
       self.assertEqual(data.json()['simple_text'], u'Lorem Ipsum')

    def test_text(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('long_text' in data.json().keys())
       self.assertEqual(data.json()['long_text'], u'Lorem Ipsum')

    def test_int(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('number1' in data.json().keys())
       self.assertEqual(data.json()['number1'], 24)

    def test_float(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('number2' in data.json().keys())
       self.assertEqual(data.json()['number2'], 11.2)

    def test_ascii(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('ascii' in data.json().keys())
       self.assertEqual(data.json()['ascii'], '1234-abc')

    def test_bool(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('tf' in data.json().keys())
       self.assertEqual(data.json()['tf'], True)

    def test_tuple(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('tuple_of' in data.json().keys())
       self.assertEqual(data.json()['tuple_of'], ['aaa', 'bbb'])

    def test_list(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('list_of' in data.json().keys())
       self.assertEqual(data.json()['list_of'], ['aaa', 'bbb'])

    def test_choice(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('choose' in data.json().keys())
       self.assertEqual(data.json()['choose'], 1)

    def test_multiple_choice(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('multiple_choice' in data.json().keys())
       self.assertEqual(data.json()['multiple_choice'], [1, 3])

    def test_unknown_type(self):
       data = IJSONifier(self.proxy)
       self.assertTrue('unknown_type' in data.json().keys())
       self.assertEqual(data.json()['unknown_type'][0].get('data_1'), u'a')
       self.assertEqual(data.json()['unknown_type'][0].get('data_2'), u'b')
