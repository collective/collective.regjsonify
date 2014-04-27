from setuptools import setup, find_packages
import os

version = '0.1.0'

tests_require = ['plone.app.testing', ]

setup(name='collective.regjsonify',
      version=version,
      description="Dump Plone registry content to a JSON format",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope3",
        "Programming Language :: Python",
        ],
      keywords='plone registry json export',
      author='keul',
      author_email='luca@keul.it',
      url='http://github.com/keul/collective.regjsonify',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'plone.registry',
          'zope.schema',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
