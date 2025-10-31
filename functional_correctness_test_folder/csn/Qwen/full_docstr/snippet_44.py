
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.exceptions import InvalidSignature


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
        self.public_key = None
        if public_key:
            self.public_key = self.convert_public_key_to_ecdsa(public_key)

    def convert_public_key_to_ecdsa(self, public_key):
        '''
        Convert the public key string to an EllipticCurvePublicKey object.
        :param public_key: verification key under Mail Settings
        :type public_key string
        :return: An EllipticCurvePublicKey object using the ECDSA algorithm
        :rtype cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        '''
        return load_pem_public_key(public_key.encode())

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
            public_key = self.public_key
        if not public_key:
            raise ValueError(
                "Public key is required for signature verification")

        message = f"{timestamp}\n{payload}".encode()
        try:
            public_key.verify(
                utils.decode_dss_signature(bytes.fromhex(signature)),
                message,
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except InvalidSignature:
            return False
