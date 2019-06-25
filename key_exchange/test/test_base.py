import cryptography
import pytest

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
