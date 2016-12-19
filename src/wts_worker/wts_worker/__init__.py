from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wts_db import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


class DatabaseTask(Task):
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()

    @property
    def session(self):
        if self._session is None:
            self._session = Session()
        return self._session
