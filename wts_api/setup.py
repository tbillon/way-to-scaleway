#!/usr/bin/env python

from setuptools import setup


setup(name='wts_api',
      version='0.0.1',
      description='SW tutorial - API',
      packages=['wts_api', 'wts_api.resources'],
      install_requires=['SQLAlchemy', 'psycopg2', 'PyYAML'],
      entry_points={
          'console_scripts': ['start-wts-api=wts_api.command_line:main'],
      })
