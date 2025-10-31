
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature
import base64


class EventWebhook:

    def __init__(self, public_key=None):
        self.public_key = None
        if public_key:
            self.public_key = self.convert_public_key_to_ecdsa(public_key)

    def convert_public_key_to_ecdsa(self, public_key):
        if isinstance(public_key, ec.EllipticCurvePublicKey):
            return public_key
        if isinstance(public_key, str):
            public_key_bytes = public_key.encode('utf-8')
        else:
            public_key_bytes = public_key
        return serialization.load_pem_public_key(public_key_bytes)

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
        if public_key is not None:
            pubkey = self.convert_public_key_to_ecdsa(public_key)
        elif self.public_key is not None:
            pubkey = self.public_key
        else:
            raise ValueError("No public key provided")

        try:
            payload_bytes = payload.encode(
                'utf-8') if isinstance(payload, str) else payload
            timestamp_bytes = timestamp.encode(
                'utf-8') if isinstance(timestamp, str) else timestamp
            signed_data = timestamp_bytes + payload_bytes
            signature_bytes = base64.b64decode(signature)
            pubkey.verify(signature_bytes, signed_data,
                          ec.ECDSA(hashes.SHA256()))
            return True
        except (InvalidSignature, ValueError, TypeError, base64.binascii.Error):
            return False
