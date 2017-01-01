"""
SW tutorial
~~~~~~~~~~~

Celery workers interface
"""
from celery import Celery, signature


worker = Celery('wts_worker',
                broker='amqp://',
                backend='rpc://', )


def broker_url(settings):
    """Return the broker url based on environment variables"""
    broker = 'amqp://'
    broker += settings.get('BROKER_USER') or 'guest'
    broker += ':' + (settings.get('BROKER_PASSWORD') or 'guest')
    broker += '@' + (settings.get('BROKER_HOST') or 'localhost')
    broker += ':' + (settings.get('BROKER_PORT') or '5672')

    return broker


def video_download_chain_task(uuid):
    """
    Create function signatures and chain them
    """
    chain = signature(
        'wts_worker.worker.video_download',
        kwargs={'uuid': uuid},
    )
    chain |= signature(
        'wts_worker.worker.video_register_title',
        kwargs={'uuid': uuid},
    )
    return chain.apply_async()
