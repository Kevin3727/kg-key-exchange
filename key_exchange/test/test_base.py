from key_exchange.src.base import KeyExchange


def test_generate_private_key():
    ke = KeyExchange()
    ke.generate_private_key()
    assert ke.public_key is not None


def test_message_encryption():
    message = b'this is a test message'
    ke = KeyExchange()
    ke.generate_private_key()
    cipher_text = ke.encrypt_message(message)
    plain_text = ke.decrypt_message(cipher_text)
    assert message == plain_text, 'plain_text must be equal to the initial ' \
                                  'message'
