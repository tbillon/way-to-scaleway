import uuid

from voluptuous import Required, Schema, MultipleInvalid
from voluptuous.validators import FqdnUrl


def UUID(value):
    return uuid.UUID(value)


uuid_validator = Schema(UUID)

def valid_uuid(value):
    try:
        uuid_validator(value)
        return True
    except MultipleInvalid as e:
        return False


task_schema_validator = Schema({Required('url'): FqdnUrl()}, )

def valid_task(task):
    try:
        task_schema_validator(task)
        return True
    except MultipleInvalid as e:
        return False
