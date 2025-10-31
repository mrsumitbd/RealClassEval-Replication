
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend


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
        self.public_key = public_key

    def convert_public_key_to_ecdsa(self, public_key):
        '''
        Convert the public key string to an EllipticCurvePublicKey object.
        :param public_key: verification key under Mail Settings
        :type public_key string
        :return: An EllipticCurvePublicKey object using the ECDSA algorithm
        :rtype cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        '''
        public_key = public_key.encode('utf-8')
        public_key = public_key.replace(b'-----BEGIN PUBLIC KEY-----', b'')
        public_key = public_key.replace(b'-----END PUBLIC KEY-----', b'')
        public_key = public_key.strip()
        public_key = base64.b64decode(public_key)
        return load_pem_public_key(
            b'-----BEGIN PUBLIC KEY-----\n' +
            base64.b64encode(public_key) + b'\n-----END PUBLIC KEY-----',
            backend=default_backend()
        )

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
            if self.public_key is None:
                raise ValueError("No public key provided")
            public_key = self.convert_public_key_to_ecdsa(self.public_key)

        message = (timestamp + payload).encode('utf-8')
        signature = base64.b64decode(signature)

        try:
            public_key.verify(
                signature,
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except:
            return False
