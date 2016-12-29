"""
wts_api.utils tests suit
"""
import random
import string
import uuid

from wts_api.utils import valid_task, valid_uuid


def test_valid_task():
    """Test that the given dictionary contains a valid URL"""
    assert valid_task({'url': 'http://www.example.com/'})


def test_invalid_task():
    """Test that the given dictionary contains an invalid URL"""
    assert not valid_task({'url': '//www.example.com/'})


def test_valid_uuid():
    """Test if the given string is a valid UUID"""
    assert valid_uuid('0597df50-cd0a-11e6-9400-6805ca24746a')


def test_invalid_uuid():
    """Test if the given string is an invalid UUID"""
    assert not valid_uuid('A1920DYEXSFA2L4PM31Z2A5EDABU08VCLS7S')
