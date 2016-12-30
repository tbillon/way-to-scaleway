"""
wts_api tests
"""
import os
import uuid
from datetime import datetime

import pytest

import wts_api
from wts_api.settings import Settings
from wts_db import config, models


@pytest.fixture(scope='module')
def initialize_api():
    """Create the Flask application & DB session
    """
    conf = Settings.load_from_file(filename='tests/credentials.yaml')
    app = wts_api.start_api()
    client = app.test_client()
    session = wts_api.session.SessionScope.init_session(keep=True)

    yield (client, session)

    session.rollback()


@pytest.fixture(scope='module')
def create_dataset(initialize_api, scope='module'):
    """Create a dataset to work on
    """
    _, session = initialize_api

    for i in range(1, 5):
        task = models.Task('http://example.com/{}'.format(i))
        session.add(task)


def test_inserted_data(initialize_api, create_dataset):
    """Test that inserted task are correct
    """
    client, session = initialize_api

    for task in session.query(models.Task).all():
        res = client.get('/task/{}'.format(task.uuid))
        assert res.status_code == 200
        assert res.get_data() == '{{"uuid": "{}"}}\n'.format(task.uuid)


def test_invalid_data(initialize_api):
    """Test that an unknown UUID return a 404 error
    """
    client, _ = initialize_api
    task_id = uuid.uuid1()
    res = client.get('/task/{}'.format(uuid))
    assert res.status_code == 404
