
import json
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = public_key

    def convert_public_key_to_ecdsa(self, public_key):
        try:
            if public_key.startswith('-----BEGIN PUBLIC KEY-----'):
                return serialization.load_pem_public_key(
                    public_key.encode(),
                    backend=default_backend()
                )
            else:
                return serialization.load_der_public_key(
                    public_key.encode(),
                    backend=default_backend()
                )
        except Exception:
            raise ValueError("Invalid public key format")

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        if public_key is None:
            if self.public_key is None:
                raise ValueError("No public key provided")
            public_key = self.public_key

        ecdsa_public_key = self.convert_public_key_to_ecdsa(public_key)

        if not isinstance(payload, str):
            payload = json.dumps(payload)

        message = f"{timestamp}{payload}".encode()

        try:
            ecdsa_public_key.verify(
                signature=signature,
                data=message,
                signature_algorithm=ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
