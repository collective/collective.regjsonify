Introduction
============

Quickly export the content of a Plone registry configuration (defined by an interface) in a Python
structure compatible with JSON format:

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
=========

The package came with a default set of know data types that cover common fields used in Plone registry.
However this set can be not complete if you are using a not supported field type.

During export operation unknown data are ignored.

If you want to export other types you must manually provide the proper ``IJSONFieldDumper`` adapter:

.. code-block:: xml

    <adapter
      factory="your.package.YouExportAdapter"
      provides="collective.regjsonify.interfaces.IJSONFieldDumper"
      for="3rd.party.field.interfaces.INewFieldType"
      />
