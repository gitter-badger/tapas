from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='tapas',
      version=version,
      description="The Tapas library.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'aiohttp',
          'click',
          'jinja2',
          'peewee',
          'colander',
          'pytest',
          'requests'
      ],
      entry_points={
        'console_scripts': [
            'tapas = tapas.scripts:main'
        ]
      },
      )
