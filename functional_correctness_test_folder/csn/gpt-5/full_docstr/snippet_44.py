import base64
from typing import Optional, Union

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey


class EventWebhook:
    '''
    This class allows you to use the Event Webhook feature. Read the docs for
    more details: https://sendgrid.com/docs/for-developers/tracking-events/event
    '''

    def __init__(self, public_key: Optional[Union[str, EllipticCurvePublicKey]] = None):
        '''
        Construct the Event Webhook verifier object
        :param public_key: verification key under Mail Settings
        :type public_key: string
        '''
        if isinstance(public_key, EllipticCurvePublicKey):
            self.public_key = public_key
        elif isinstance(public_key, str):
            self.public_key = self.convert_public_key_to_ecdsa(public_key)
        elif public_key is None:
            self.public_key = None
        else:
            raise TypeError(
                "public_key must be a string, EllipticCurvePublicKey, or None")

    def convert_public_key_to_ecdsa(self, public_key):
        '''
        Convert the public key string to an EllipticCurvePublicKey object.
        :param public_key: verification key under Mail Settings
        :type public_key string
        :return: An EllipticCurvePublicKey object using the ECDSA algorithm
        :rtype cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        '''
        if isinstance(public_key, EllipticCurvePublicKey):
            return public_key
        if not isinstance(public_key, (str, bytes)):
            raise TypeError("public_key must be a PEM string or bytes")

        pem_bytes = public_key.encode(
            "utf-8") if isinstance(public_key, str) else public_key
        key = serialization.load_pem_public_key(pem_bytes)
        if not isinstance(key, EllipticCurvePublicKey):
            raise ValueError(
                "Provided public key is not an EllipticCurvePublicKey")
        return key

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
        key = public_key or self.public_key
        if key is None:
            raise ValueError(
                "A public key must be provided either at initialization or as an argument.")

        if isinstance(key, (str, bytes)):
            key = self.convert_public_key_to_ecdsa(key)
        elif not isinstance(key, EllipticCurvePublicKey):
            raise TypeError(
                "public_key must be an EllipticCurvePublicKey, PEM string, or bytes")

        if isinstance(timestamp, bytes):
            ts_bytes = timestamp
        elif isinstance(timestamp, str):
            ts_bytes = timestamp.encode("utf-8")
        else:
            raise TypeError("timestamp must be a string or bytes")

        if isinstance(payload, bytes):
            payload_bytes = payload
        elif isinstance(payload, str):
            payload_bytes = payload.encode("utf-8")
        else:
            raise TypeError("payload must be a string or bytes")

        if isinstance(signature, str):
            try:
                sig_bytes = base64.b64decode(signature, validate=True)
            except Exception:
                # try URL-safe base64 without padding
                try:
                    sig_bytes = base64.urlsafe_b64decode(signature + "===")
                except Exception:
                    return False
        elif isinstance(signature, bytes):
            sig_bytes = signature
        else:
            raise TypeError("signature must be a string or bytes")

        message = ts_bytes + payload_bytes

        try:
            key.verify(sig_bytes, message, ec.ECDSA(hashes.SHA256()))
            return True
        except (InvalidSignature, ValueError):
            return False
