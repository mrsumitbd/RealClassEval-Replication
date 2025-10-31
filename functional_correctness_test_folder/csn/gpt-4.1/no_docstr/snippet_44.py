
import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = public_key

    def convert_public_key_to_ecdsa(self, public_key):
        # Remove header/footer and newlines
        public_key = public_key.strip().replace("-----BEGIN PUBLIC KEY-----",
                                                "").replace("-----END PUBLIC KEY-----", "").replace("\n", "")
        key_bytes = base64.b64decode(public_key)
        return serialization.load_der_public_key(key_bytes)

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        if public_key is None:
            public_key = self.public_key
        if public_key is None:
            raise ValueError("Public key is required for verification.")
        ecdsa_public_key = self.convert_public_key_to_ecdsa(public_key)
        signed_payload = f"{timestamp}{payload}".encode("utf-8")
        decoded_signature = base64.b64decode(signature)
        try:
            ecdsa_public_key.verify(
                decoded_signature,
                signed_payload,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
