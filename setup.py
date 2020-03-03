# -*- coding: utf-8 -*-
"""
This module contains the tool of pcp.contenttypes
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('src', 'pcp', 'contenttypes', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing', 'plone.testing', 'plone.app.testing', 'robotsuite',
                 'robotframework-selenium2library', 'Products.PloneTestCase', 'mock']

setup(name='pcp.contenttypes',
      version=version,
      description="Content types for the Project Coordination Portal application",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        ],
      keywords='Plone EUDAT Project Coordination',
      author='Raphael Ritz',
      author_email='raphael.ritz@gmail.com',
      url='https://github.com/raphael-ritz/eudat.pcp.site',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['pcp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'pint',
                        'Products.ATExtensions',
                        'Products.ATBackRef',
                        'Products.ATReferenceBrowserWidget',
                        'Products.MasterSelectWidget',
                        'Products.ATVocabularyManager',
                        'plone.formwidget.contenttree',
                        'collective.handleclient',
                        'collective.monkeypatcher',
                        'incf.countryutils',
                        'semantic_version',
                        # 'uwosh.pfg.d2c',
                        'furl',
                        'zopyx.plone.persistentlogger',
                        'z3c.jbot',
                        'plone.formwidget.datetime',
                        'collective.dexteritytextindexer',
                        'collective.z3cform.datagridfield',
                        ],
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      test_suite='pcp.contenttypes.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["templer.localcommands"],
      )
