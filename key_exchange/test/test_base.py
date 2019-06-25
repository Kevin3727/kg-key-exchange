import os
from pathlib import Path

import cryptography
import pytest

from key_exchange.src import pass_management
from key_exchange.src.base import KeyExchange


def test_version():
    assert float(cryptography.__version__) >= 2.7, \
        'cryptography library is out of date, download version 2.7 of later!'


def test_generate_private_key():
    ke = KeyExchange()
    ke.generate_private_key()
    assert ke.public_key is not None


def test_security():
    ke = KeyExchange()
    with pytest.raises(AttributeError) as e_info:
        # private key should not be public
        ke.__private_key


def test_message_encryption():
    message = b'this is a test message'
    ke = KeyExchange()
    ke.generate_private_key()
    cipher_text = ke.encrypt_message(message)
    plain_text = ke.decrypt_message(cipher_text)
    assert message == plain_text, \
        'plain_text must be equal to the initial message!'


def test_get_public_bytes():
    ke = KeyExchange()
    ke.generate_private_key()
    if not isinstance(ke.get_public_bytes(ke.public_key), bytes):
        raise TypeError('get_public_bytes must return bytes!')


def test_client_packet():
    pass_management.create_password('password', 'pytest_username', loc='data/')

    # server authentication
    ke = KeyExchange()
    ke.generate_private_key()
    assert ke.authenticate_client(
        'pytest_username',
        ke.client_packet('password', ke.public_key),
        loc='data/')

    # client authentication
    ke_client = KeyExchange()
    ke_client.generate_private_key()

    hashed_pass = pass_management.get_hashed_password('pytest_username',
                                                      loc='data/')
    server_packet = ke.server_packet(hashed_pass, ke_client.public_key)

    assert ke_client.authenticate_server('password', server_packet)

    # cleanup
    os.remove(
        str(Path(pass_management.get_location('pytest_username', 'data/'))))
