"""
* Copyright (c) 2019 Kevin Ghorbani. All rights reserved.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from key_exchange.src.pass_management import hash_bytes, get_hashed_password


class KeyExchange:
    def __init__(self):
        self.__private_key = None
        self.public_key = None

    def client_packet(self, password, server_public_key):
        public_bytes = self.get_public_bytes(server_public_key)
        hashed_password = hash_bytes(password.encode())

        new_pass = hashed_password + public_bytes
        return self.encrypt_message(hash_bytes(new_pass))

    def decrypt_message(self, cipher_text):
        return self.__private_key.decrypt(
            cipher_text,
            padding.OAEP(
                padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )

    def encrypt_message(self, message):
        return self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        )

    def generate_private_key(self):
        self.__private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.__private_key.public_key()

    @staticmethod
    def get_public_bytes(public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.PKCS1)

    def authenticate_client(self, username, client_packet, loc='data/'):
        public_bytes = self.get_public_bytes(self.public_key)
        hashed_password = get_hashed_password(username, loc)

        new_pass = hashed_password + public_bytes
        return hash_bytes(new_pass) == self.decrypt_message(client_packet)
