import os
from pathlib import Path

import pytest

from key_exchange.src import pass_management


def test_get_location():
    assert pass_management.get_location('name', '../test_loc/') == \
           '../test_loc/name.dat'


def test_create_password():
    assert pass_management.create_password('password', 'username',
                                           loc='data/') is None

    assert Path(pass_management.get_location(
        'username', 'data/')).is_file(), 'File does not exist!'

    with pytest.raises(UnicodeDecodeError) as e_info:
        with open(pass_management.get_location('username', 'data/'), 'r') as f:
            f.read()

    with open(pass_management.get_location('username', 'data/'),
              'rb') as f:
        if not isinstance(f.read(), bytes):
            assert OSError('file is not a binary')

    os.remove(str(Path(pass_management.get_location('username', 'data/'))))
