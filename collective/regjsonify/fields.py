# -*- coding: utf8 -*-

from .interfaces import IJSONFieldDumper
from plone.registry.interfaces import IRecordsProxy
from zope.interface import implementer


@implementer(IJSONFieldDumper)
class Base(object):
    """
    The basic implementation.
    Can be used when the data is JSON compatible
    """

    def __init__(self, field):
        self.field = field

    def data(self, record):
        if IRecordsProxy.providedBy(record):
            return getattr(record, self.field.__name__)
        return record


@implementer(IJSONFieldDumper)
class Sequence(Base):
    """
    ISequence implementation (common for IList and ITuple).
    Iterate on elements and recursively call IJSONFieldDumper on subdata
    """

    def data(self, record):
        result = []
        field = self.field
        if IRecordsProxy.providedBy(record):
            name = field.__name__
            sequence = getattr(record, name)
        else:
            sequence = record
        for x in sequence:
            try:
                subfield_data = IJSONFieldDumper(field.value_type)
            except TypeError:
                continue
            result.append(subfield_data.data(x))
        return result


@implementer(IJSONFieldDumper)
class Object(Base):
    """
    The IObject implementation: try to extract JSON from the inner schema
    """

    def data(self, record):
        field = self.field
        result = {}
        for name, subfield in field.schema.namesAndDescriptions():
            try:
                subfield_data = IJSONFieldDumper(subfield)
            except TypeError:
                continue
            result[name] = subfield_data.data(getattr(record, name))
        return result
