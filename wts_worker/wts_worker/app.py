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

import wts_worker
from wts_worker.settings import Settings, broker_url


app = Celery('wts_worker',
             broker='amqp://',
             backend='rpc://',
             include=['wts_worker.worker'])


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
    wts_worker.DatabaseTask.init_database()
    app.start()


if __name__ == '__main__':
    main()
