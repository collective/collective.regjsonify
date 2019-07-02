# -*- coding: utf8 -*-

from .interfaces import IJSONifier
from .interfaces import IJSONFieldDumper
from zope.interface import implementer


@implementer(IJSONifier)
class JSONifier(object):
    """
    Default IJSONifier implementation.
    Iterate registry data and dump every field looking at its type
    """

    def __init__(self, settings):
        self.settings = settings

    def _iterateAttributes(self, schema):
        data = []
        for attr in schema.namesAndDescriptions():
            data.append(attr)
        for parent in schema.getBases():
            data.extend(self._iterateAttributes(parent))
        return data

    def json(self):
        result = {}
        settings = self.settings
        registry_data = self._iterateAttributes(settings.__schema__)
        for name, data in registry_data:
            try:
                field_data = IJSONFieldDumper(data)
                result[name] = field_data.data(settings)
            except TypeError:
                continue
        return result
