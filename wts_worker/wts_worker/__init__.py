from __future__ import absolute_import, unicode_literals

from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wts_db import config
from wts_worker.settings import Settings


class DatabaseTask(Task):
    """
    Celery Task handling database connection
    """
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()

    @property
    def session(self):
        if self._session is None:
            self._session = self.Session()
        return self._session

    @classmethod
    def init_database(cls):
        """
        Create SQLAlchemy Engine & Session when needed
        """
        conn = config.db_connection_string(Settings)
        cls.Engine = create_engine(conn, echo=Settings.get('DEBUG'))
        cls.Session = sessionmaker(bind=cls.Engine)
        return cls
