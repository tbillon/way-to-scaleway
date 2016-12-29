import pytest

from wts_db import config


@pytest.fixture(scope='module')
def setup_defaults():
    DEFAULTS = {'DATABASE_USER': 'postgres',
                'DATABASE_PASSWORD': 'postgres', }
    return config.ConfigLoader(defaults=DEFAULTS)


def test_db_connection_string(setup_defaults):
    conn = config.db_connection_string(setup_defaults)
    assert conn == 'postgresql+psycopg2://postgres:postgres@localhost/postgres'


def test_dict_get(setup_defaults):
    assert setup_defaults.get('DATABASE_USER') == 'postgres'


def test_dict_get_unknown(setup_defaults):
    assert setup_defaults.get('UNKNOW') is None


def test_load_from_file(setup_defaults):
    setup_defaults.load_from_file('tests/credentials.yaml')
    conn = config.db_connection_string(setup_defaults)
    assert conn == 'postgresql+psycopg2://user:password@host/db'
