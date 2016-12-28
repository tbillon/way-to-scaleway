"""
SW tutorial
~~~~~~~~~~~

API settings
"""
from wts_db import config


DEFAULTS = {'DEBUG': False, 'OUTPUT_DIRECTORY': '/videos/incoming'}


Settings = config.ConfigLoader(defaults=DEFAULTS)
