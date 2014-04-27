# -*- coding: utf8 -*-

from zope.interface import Interface


class IJSONifier(Interface):
    """An object able to dump a registry sheet (commonly a plone.registry IRecordsProxy object)"""

    def json():
        """Return Python structure, ready for be dumper in JSON"""


class IJSONFieldDumper(Interface):
    """An object that can convert a single registry entry to Python data
    (so: later we can translate this to JSON)
    """

    def data(record):
        """Return entry converted to Python data, extracted from record"""
