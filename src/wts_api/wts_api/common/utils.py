from collections import OrderedDict
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


def my_marshal(data, fields, envelope=None):
    """Filter unasigned keys"""
    def make(cls):
        if isinstance(cls, type):
            return cls()
        return cls

    if isinstance(data, (list, tuple)):
        return (OrderedDict([(envelope, [my_marshal(d, fields) for d in data])])
                if envelope else [my_marshal(d, fields) for d in data])

    items = ((k, my_marshal(data, v) if isinstance(v, dict)
            else make(v).output(k, data))
             for k, v in fields.items())
    items = ((k,v) for k, v in items if v is not None)
    return OrderedDict([(envelope, OrderedDict(items))]) if envelope else OrderedDict(items)
