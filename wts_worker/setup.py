#!/usr/bin/env python

from setuptools import setup


setup(name='wts_worker',
      version='0.0.1',
      description='SW tutorial - Worker',
      packages=['wts_worker'],
      install_requires=['SQLAlchemy', 'psycopg2', 'PyYAML', 'celery'],
      entry_points={
          'console_scripts': ['start-wts-worker=wts_worker.app:main'],
      })
