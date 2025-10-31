
import base64
from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.exceptions import InvalidSignature


class EventWebhook:
    """
    This class allows you to use the Event Webhook feature. Read the docs for
    more details: https://sendgrid.com/docs/for-developers/tracking-events/event
    """

    def __init__(self, public_key: Optional[str] = None):
        """
        Construct the Event Webhook verifier object
        :param public_key: verification key under Mail Settings
        :type public_key: string
        """
        self._public_key_obj: Optional[ec.EllipticCurvePublicKey] = None
        if public_key is not None:
            self._public_key_obj = self.convert_public_key_to_ecdsa(public_key)

    @staticmethod
    def convert_public_key_to_ecdsa(public_key: str) -> ec.EllipticCurvePublicKey:
        """
        Convert the public key string to an EllipticCurvePublicKey object.
        :param public_key: verification key under Mail Settings
        :type public_key string
        :return: An EllipticCurvePublicKey object using the ECDSA algorithm
        :rtype cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey
        """
        # The key is base64 encoded DER
        der_bytes = base64.b64decode(public_key)
        return load_der_public_key(der_bytes)

    def verify_signature(
        self,
        payload: str,
        signature: str,
        timestamp: str,
        public_key: Optional[ec.EllipticCurvePublicKey] = None,
    ) -> bool:
        """
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
        """
        if public_key is None:
            if self._public_key_obj is None:
                raise ValueError("Public key not provided")
            public_key = self._public_key_obj

        # Build the message that was signed: "<timestamp>.<payload>"
        message = f"{timestamp}.{payload}".encode("utf-8")

        # Decode the base64 signature
        try:
            signature_bytes = base64.b64decode(signature)
        except Exception:
            return False

        try:
            public_key.verify(signature_bytes, message,
                              ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
        except Exception:
            # Any other error (e.g., wrong key type) should be treated as invalid
            return False
