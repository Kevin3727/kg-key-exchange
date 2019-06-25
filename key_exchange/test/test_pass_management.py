import hashlib
import os
from pathlib import Path

import pytest

from key_exchange.src import pass_management


def test_get_location():
    assert pass_management.get_location('name', '../test_loc/') == \
           '../test_loc/name.dat'


def test_create_password():
    assert pass_management.create_password('password', 'pytest_username',
                                           loc='data/') is None

    assert Path(pass_management.get_location(
        'pytest_username', 'data/')).is_file(), 'File does not exist!'

    with pytest.raises(UnicodeDecodeError) as e_info:
        with open(pass_management.get_location('pytest_username', 'data/'),
                  'r') as f:
            f.read()

    with open(pass_management.get_location('pytest_username', 'data/'),
              'rb') as f:
        if not isinstance(f.read(), bytes):
            assert OSError('file is not a binary')

    os.remove(
        str(Path(pass_management.get_location('pytest_username', 'data/'))))


def test_get_hashed_password():
    pass_management.create_password('password', 'pytest_username', loc='data/')
    hashed_pass = hashlib.sha256('password'.encode()).digest()
    read_hashed_pass = pass_management.get_hashed_password('pytest_username',
                                                           loc='data/')

    assert hashed_pass == read_hashed_pass, 'Hashed passwords do not match!'
    assert pass_management.get_hashed_password('Invalid_user',
                                               loc='data/') is None, \
        'Invalid username must return None'

    os.remove(
        str(Path(pass_management.get_location('pytest_username', 'data/'))))
