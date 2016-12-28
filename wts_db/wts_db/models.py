"""
SW tutorial
~~~~~~~~~~~

Database models.
"""

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Task(Base):
    """
    Describe a task

    Attributes:
        uuid    Task unique identifier
        sub_date        Date & time of submition
        dst_url         Local URL
        src_url         Source URL
        title           Video title
    """
    __tablename__ = 'task'

    uuid = sa.Column(UUID,
                     primary_key=True,
                     server_default=sa.sql.expression.text('uuid_generate_v1mc()'))
    sub_date = sa.Column(sa.DateTime,
                         nullable=False,
                         server_default=sa.func.current_timestamp())
    dst_url = sa.Column(sa.String(2083), nullable=True)
    src_url = sa.Column(sa.String(2083), nullable=False)
    title = sa.Column(sa.String(100), nullable=True)

    def __init__(self, url):
        self.src_url = url
