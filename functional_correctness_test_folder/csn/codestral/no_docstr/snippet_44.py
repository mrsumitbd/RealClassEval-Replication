
import json
import ecdsa
import base64
import hashlib


class EventWebhook:

    def __init__(self, public_key=None):

        self.public_key = public_key
        self.ecdsa_public_key = self.convert_public_key_to_ecdsa(
            public_key) if public_key else None

    def convert_public_key_to_ecdsa(self, public_key):

        public_key_bytes = base64.b64decode(public_key)
        return ecdsa.VerifyingKey.from_string(public_key_bytes, curve=ecdsa.SECP256k1)

    def verify_signature(self, payload, signature, timestamp, public_key=None):

        if public_key:
            ecdsa_public_key = self.convert_public_key_to_ecdsa(public_key)
        elif self.ecdsa_public_key:
            ecdsa_public_key = self.ecdsa_public_key
        else:
            raise ValueError("Public key is required")

        message = f"{timestamp}.{json.dumps(payload, separators=(',', ':'))}".encode(
            'utf-8')
        signature_bytes = base64.b64decode(signature)

        return ecdsa_public_key.verify(signature_bytes, message, hashfunc=hashlib.sha256)
