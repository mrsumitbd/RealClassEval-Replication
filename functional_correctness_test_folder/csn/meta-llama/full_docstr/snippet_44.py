
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import base64


class EventWebhook:
    '''
    This class allows you to use the Event Webhook feature. Read the docs for
    more details: https://sendgrid.com/docs/for-developers/tracking-events/event
    '''

    def __init__(self, public_key=None):
        '''
        Construct the Event Webhook verifier object
        :param public_key: verification key under Mail Settings
        :type public_key: string
        '''
        self.public_key = self.convert_public_key_to_ecdsa(
            public_key) if public_key else None

    def convert_public_key_to_ecdsa(self, public_key):
        '''
        Convert the public key string to an EllipticCurvePublicKey object.
        :param public_key: verification key under Mail Settings
        :type public_key string
        :return: An EllipticCurvePublicKey object using the ECDSA algorithm
        :rtype cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        '''
        if not public_key:
            raise ValueError("Public key is required")

        try:
            public_key_bytes = public_key.encode('ascii')
            public_key_loaded = serialization.load_pem_public_key(
                public_key_bytes)
            if not isinstance(public_key_loaded, ec.EllipticCurvePublicKey):
                raise ValueError(
                    "Public key is not an Elliptic Curve public key")
            return public_key_loaded
        except ValueError as e:
            raise ValueError("Invalid public key: {}".format(str(e)))

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
        if not public_key:
            if not self.public_key:
                raise ValueError("Public key is required")
            public_key = self.public_key

        try:
            signature_bytes = base64.b64decode(signature)
            payload_bytes = (timestamp + payload).encode('utf-8')
            public_key.verify(signature_bytes, payload_bytes,
                              ec.ECDSA(hashes.SHA256()))
            return True
        except (ValueError, InvalidSignature):
            return False
