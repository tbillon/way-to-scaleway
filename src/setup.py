#!/usr/bin/env python

import setuptools
from setuptools import setup, find_packages


setup(name='wts',
      version='0.0.1',
      description='SW training project',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['run-wts-api=wts_api.command_line:main'],
    }
)
