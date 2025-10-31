
from cryptography.hazmat.primitives import serialization, hashes
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
        if public_key is None:
            if self.public_key is None:
                raise ValueError("Public key is required")
            public_key = self.public_key
        else:
            public_key = self.convert_public_key_to_ecdsa(public_key)

        try:
            signature_bytes = bytes.fromhex(signature)
        except ValueError:
            return False

        try:
            public_key.verify(
                signature_bytes,
                (timestamp + payload).encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
