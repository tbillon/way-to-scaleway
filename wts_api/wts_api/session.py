"""
SW tutorial
~~~~~~~~~~~

Database session context manager
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wts_api.settings import Settings
from wts_db import config


class SessionScope(object):
    """Create database session when needed
    """
    _session = None

    def __enter__(self):
        if self._session is None:
            self._session = self.Session()
        return self._session

    def __exit__(self, type, value, traceback):
        if self._session is not None:
            self._session.close()

    @classmethod
    def init_database(cls):
        """
        Create SQLAlchemy Engine & Session when needed
        """
        conn = config.db_connection_string(Settings)
        cls.Engine = create_engine(conn, echo=Settings.get('DEBUG'))
        cls.Session = sessionmaker(bind=cls.Engine)
        return cls
