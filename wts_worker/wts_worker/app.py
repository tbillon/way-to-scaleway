"""
SW tutorial
~~~~~~~~~~~

SW Celery launcher

Start it with:
    $ start-wts-worker -A wts_worker.app worker -l info
"""
import os
import sys

from celery import Celery
from elasticsearch import Elasticsearch

import wts_worker
from wts_worker.settings import Settings, broker_url, es_connection


app = Celery('wts_worker',
             broker='amqp://',
             backend='rpc://',
             include=['wts_worker.worker'])
es = Elasticsearch()

def main():
    """Program entry point
    """
    credentials = os.environ.get('CREDENTIALS')
    if credentials is None:
        print 'Could not load credentials file'
        sys.exit(1)
    Settings.load_from_file(credentials)

    app.conf.update(
        broker_url=broker_url(Settings),
    )

    # Init database connection
    wts_worker.DatabaseTask.init_database()

    # Create the Elasticsearch connection
    es.transport.add_connection(es_connection(Settings))

    # Start the workers
    app.start()


if __name__ == '__main__':
    main()
