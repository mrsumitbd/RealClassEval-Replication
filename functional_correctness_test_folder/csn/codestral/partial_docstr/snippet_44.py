
import base64
import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = self.convert_public_key_to_ecdsa(
            public_key) if public_key else None

    def convert_public_key_to_ecdsa(self, public_key):
        if isinstance(public_key, ec.EllipticCurvePublicKey):
            return public_key
        elif isinstance(public_key, str):
            public_key_bytes = base64.b64decode(public_key)
            return serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
        else:
            raise ValueError("Unsupported public key format")

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        if not public_key:
            if not self.public_key:
                raise ValueError("Public key is required")
            public_key = self.public_key

        message = timestamp + payload
        message_bytes = message.encode('utf-8')
        signature_bytes = base64.b64decode(signature)

        try:
            public_key.verify(
                signature_bytes,
                message_bytes,
                ec.ECDSA(hashlib.sha256())
            )
            return True
        except:
            return False
