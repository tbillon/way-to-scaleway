"""
SW tutorial
~~~~~~~~~~~

Worker settings
"""
from wts_db import config


DEFAULTS = {'DEBUG': False, 'OUTPUT_DIRECTORY': '/videos/incoming',
            'SEARCH_HOST': 'localhost', 'SEARCH_PORT': 9200, }


Settings = config.ConfigLoader(defaults=DEFAULTS)


def broker_url(settings):
    """Return the broker url based on environment variables"""
    broker = 'amqp://'
    broker += settings.get('BROKER_USER') or 'guest'
    broker += ':' + (settings.get('BROKER_PASSWORD') or 'guest')
    broker += '@' + (settings.get('BROKER_HOST') or 'localhost')
    broker += ':' + (settings.get('BROKER_PORT') or '5672')

    return broker

def es_connection(settings):
    return {'host': settings.get('SEARCH_HOST') or 'localhost',
            'port': settings.get('SEARCH_PORT') or 9200}
