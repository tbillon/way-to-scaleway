from datetime import datetime

from sqlalchemy import Column, DateTime, FetchedValue, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'

    uuid = Column(UUID, primary_key=True, server_default=FetchedValue())
    sub_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    upd_date = Column(DateTime, nullable=True)
    status = Column(Integer, default=0)
    dst_url = Column(String(2083), nullable=True)
    src_url = Column(String(2083), nullable=False)

    def __init__(self, url):
        self.src_url = url


if __name__ == '__main__':
    task = Task('http://example.com/')
    print Task.__table__
