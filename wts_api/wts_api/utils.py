"""
SW tutorial
~~~~~~~~~~~

Validation functions
"""
import uuid

from voluptuous import Required, Schema, MultipleInvalid
from voluptuous.validators import FqdnUrl


def create_uuid(value):
    """
    Return an UUID from value
    """
    return uuid.UUID(value)


def valid_uuid(value):
    """
    Control that an UUID is valid

    """
    uuid_validator = Schema(create_uuid)
    try:
        uuid_validator(value)
        return True
    except MultipleInvalid:
        return False


def valid_task(task):
    """
    Control that POST task data is correct
    """
    task_schema_validator = Schema({Required('url'): FqdnUrl()}, )
    try:
        task_schema_validator(task)
        return True
    except MultipleInvalid:
        return False
