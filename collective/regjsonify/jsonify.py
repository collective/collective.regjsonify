# -*- coding: utf8 -*-

from .interfaces import IJSONifier
from .interfaces import IJSONFieldDumper
from zope.interface import implements
from zope.component.interfaces import ComponentLookupError


class JSONifier(object):
    """
    Default IJSONifier implementation.
    Iterate registry data and dump every field looking at it's type
    """
    implements(IJSONifier)

    def __init__(self, settings):
        self.settings = settings

    def json(self):
        result = {}
        settings = self.settings
        registry_data = settings.__schema__.namesAndDescriptions()
        for name, data in registry_data:
            try:
                field_data = IJSONFieldDumper(data)
                result[name] = field_data.data(settings)
            except TypeError:
                continue
        return result
