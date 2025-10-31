
import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend


class EventWebhook:

    def __init__(self, public_key=None):
        if public_key:
            self.public_key = self.convert_public_key_to_ecdsa(public_key)
        else:
            self.public_key = None

    def convert_public_key_to_ecdsa(self, public_key):
        try:
            return serialization.load_pem_public_key(
                public_key.encode(),
                backend=default_backend()
            )
        except ValueError:
            raise ValueError("Invalid public key")

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        if public_key:
            ecdsa_public_key = self.convert_public_key_to_ecdsa(public_key)
        elif self.public_key:
            ecdsa_public_key = self.public_key
        else:
            raise ValueError("Public key is required")

        signed_payload = timestamp + payload
        try:
            ecdsa_public_key.verify(
                bytes.fromhex(signature),
                signed_payload.encode(),
                ec.ECDSA(hashlib.sha256())
            )
            return True
        except (InvalidSignature, ValueError):
            return False
