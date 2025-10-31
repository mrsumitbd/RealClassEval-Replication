
import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = public_key

    def convert_public_key_to_ecdsa(self, public_key):
        try:
            return serialization.load_pem_public_key(public_key.encode())
        except ValueError:
            raise ValueError("Invalid public key format")

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        '''
        Verify signed event webhook requests.
        :param payload: event payload in the request body
        :type payload: string
        :param signature: value obtained from the 'X-Twilio-Email-Event-Webhook-Signature' header
        :type signature: string
        :param timestamp: value obtained from the 'X-Twilio-Email-Event-Webhook-Timestamp' header
        :type timestamp: string
        :param public_key: elliptic curve public key
        :type public_key: cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        :return: true or false if signature is valid
        '''
        if public_key is None:
            public_key = self.public_key
        if public_key is None:
            raise ValueError("No public key provided")

        if not isinstance(public_key, ec.EllipticCurvePublicKey):
            public_key = self.convert_public_key_to_ecdsa(public_key)

        message = f"{timestamp}{payload}".encode('utf-8')
        try:
            public_key.verify(
                bytes.fromhex(signature),
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False
