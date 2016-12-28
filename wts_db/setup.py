#!/usr/bin/env python

from setuptools import setup


setup(name='wts_db',
      version='0.0.1',
      description='SW tutorial - db models',
      packages=['wts_db'],
      install_requires=['SQLAlchemy', 'psycopg2', 'PyYAML'])
