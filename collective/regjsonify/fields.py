# -*- coding: utf8 -*-

from .interfaces import IJSONFieldDumper
from plone.registry.interfaces import IRecordsProxy
from zope.interface import implements


class Base(object):
    """
    The basic implementation.
    Can be used when the data is JSON compatible
    """
    implements(IJSONFieldDumper)
    
    def __init__(self, field):
        self.field = field

    def data(self, record):
        if IRecordsProxy.providedBy(record):
            return getattr(record, self.field.__name__)
        return record


class Sequence(Base):
    """
    ISequence implementation (common for IList and ITuple).
    Iterate on elements and recursively call IJSONFieldDumper on subdata
    """
    implements(IJSONFieldDumper)
    
    def data(self, record):
        result = []
        field = self.field
        name = field.__name__
        for x in getattr(record, name):
            try:
                subfield_data = IJSONFieldDumper(field.value_type)
                result.append(subfield_data.data(x))
            except TypeError:
                continue
        return result

