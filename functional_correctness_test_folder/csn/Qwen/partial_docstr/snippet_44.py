
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.backends import default_backend
import base64
import hashlib


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = self.convert_public_key_to_ecdsa(
            public_key) if public_key else None

    def convert_public_key_to_ecdsa(self, public_key):
        if not public_key:
            return None
        try:
            # Assuming public_key is in PEM format
            return serialization.load_pem_public_key(
                public_key.encode(),
                backend=default_backend()
            )
        except Exception as e:
            raise ValueError("Invalid public key format") from e

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        public_key = public_key or self.public_key
        if not public_key:
            raise ValueError("Public key is required to verify signature")

        # Create the message to be verified
        message = f"{timestamp}\n{payload}"
        message_bytes = message.encode('utf-8')

        # Decode the base64 encoded signature
        signature_bytes = base64.b64decode(signature)

        try:
            # Verify the signature
            public_key.verify(
                signature_bytes,
                message_bytes,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False
