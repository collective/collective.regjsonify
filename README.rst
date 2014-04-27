Quickly export the content of a Plone registry set of configuration (defined by an interface)
in a Python structure compatible with JSON format:

.. code-block:: python

    import json
    from collective.regjsonify.interfaces import IJSONifier
    from plone.registry.interfaces import IRegistry
    from zope.component import queryUtility
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IYouInterfaceSettings)
    python_data = IJSONifier(settings).json()
    json_data = json.dumps(python_data)

Extending
---------

The package came with a default set of know data types. This set can be not complete and if an unknow type
in found during the export, it will be ignored.

If you want to export other types you must manually provide the proper ``IJSONFieldDumper`` adapter.
