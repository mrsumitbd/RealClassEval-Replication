
from ecdsa import VerifyingKey, SECP256k1
import hashlib
import base64
import hmac


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = public_key
        if self.public_key:
            self.verifying_key = self.convert_public_key_to_ecdsa(
                self.public_key)
        else:
            self.verifying_key = None

    def convert_public_key_to_ecdsa(self, public_key):
        return VerifyingKey.from_string(base64.b64decode(public_key), curve=SECP256k1)

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        if public_key:
            verifying_key = self.convert_public_key_to_ecdsa(public_key)
        elif self.verifying_key:
            verifying_key = self.verifying_key
        else:
            raise ValueError(
                "Public key must be provided either during initialization or in the method call.")

        message = f"{timestamp}.{payload}"
        signature_bytes = base64.b64decode(signature)
        return verifying_key.verify(signature_bytes, message.encode(), hashfunc=hashlib.sha256)
