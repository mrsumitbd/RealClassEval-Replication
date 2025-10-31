from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_v1_5, AES
import json
from Crypto.Random import get_random_bytes
from lxml import etree

class EncryptedPayload:
    """Diaspora encrypted JSON payloads."""

    @staticmethod
    def decrypt(payload, private_key):
        """Decrypt an encrypted JSON payload and return the Magic Envelope document inside."""
        cipher = PKCS1_v1_5.new(private_key)
        aes_key_str = cipher.decrypt(b64decode(payload.get('aes_key')), sentinel=None)
        aes_key = json.loads(aes_key_str.decode('utf-8'))
        key = b64decode(aes_key.get('key'))
        iv = b64decode(aes_key.get('iv'))
        encrypted_magic_envelope = b64decode(payload.get('encrypted_magic_envelope'))
        encrypter = AES.new(key, AES.MODE_CBC, iv)
        content = encrypter.decrypt(encrypted_magic_envelope)
        return etree.fromstring(pkcs7_unpad(content))

    @staticmethod
    def get_aes_key_json(iv, key):
        return json.dumps({'key': b64encode(key).decode('ascii'), 'iv': b64encode(iv).decode('ascii')}).encode('utf-8')

    @staticmethod
    def get_iv_key_encrypter():
        iv = get_random_bytes(AES.block_size)
        key = get_random_bytes(32)
        encrypter = AES.new(key, AES.MODE_CBC, iv)
        return (iv, key, encrypter)

    @staticmethod
    def encrypt(payload, public_key):
        """
        Encrypt a payload using an encrypted JSON wrapper.

        See: https://diaspora.github.io/diaspora_federation/federation/encryption.html

        :param payload: Payload document as a string.
        :param public_key: Public key of recipient as an RSA object.
        :return: Encrypted JSON wrapper as dict.
        """
        iv, key, encrypter = EncryptedPayload.get_iv_key_encrypter()
        aes_key_json = EncryptedPayload.get_aes_key_json(iv, key)
        cipher = PKCS1_v1_5.new(public_key)
        aes_key = b64encode(cipher.encrypt(aes_key_json))
        padded_payload = pkcs7_pad(payload.encode('utf-8'), AES.block_size)
        encrypted_me = b64encode(encrypter.encrypt(padded_payload))
        return {'aes_key': aes_key.decode('utf-8'), 'encrypted_magic_envelope': encrypted_me.decode('utf8')}