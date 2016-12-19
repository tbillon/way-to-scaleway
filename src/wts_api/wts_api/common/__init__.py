from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wts_db import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)


class SessionScope:
    _session = None

    def __enter__(self):
        if self._session is None:
            self._session = Session()
        return self._session

    def __exit__(self, type, value, traceback):
        if self._session is not None:
            self._session.close()
