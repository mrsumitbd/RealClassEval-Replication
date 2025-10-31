
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


class EventWebhook:
    """
    Utility class for verifying Twilio Email Event Webhook signatures.
    """

    def __init__(self, public_key=None):
        """
        Initialize the EventWebhook with an optional public key.
        :param public_key: PEM encoded public key string or bytes, or an already
                           loaded EllipticCurvePublicKey instance.
        """
        self.public_key = None
        if public_key is not None:
            self.public_key = self.convert_public_key_to_ecdsa(public_key)

    def convert_public_key_to_ecdsa(self, public_key):
        """
        Convert a PEM encoded public key to an EllipticCurvePublicKey instance.
        :param public_key: PEM string, bytes, or EllipticCurvePublicKey.
        :return: EllipticCurvePublicKey instance.
        """
        if isinstance(public_key, ec.EllipticCurvePublicKey):
            return public_key

        if isinstance(public_key, str):
            public_key_bytes = public_key.encode("utf-8")
        elif isinstance(public_key, (bytes, bytearray)):
            public_key_bytes = public_key
        else:
            raise TypeError(
                "public_key must be a PEM string, bytes, or EllipticCurvePublicKey")

        return serialization.load_pem_public_key(public_key_bytes)

    def verify_signature(self, payload, signature, timestamp, public_key=None):
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
        :return: True if signature is valid, False otherwise
        """
        # Use provided public key or the one stored in the instance
        key = public_key or self.public_key
        if key is None:
            raise ValueError(
                "No public key provided for signature verification")

        # Decode the base64 signature
        try:
            signature_bytes = base64.b64decode(signature)
        except Exception as e:
            raise ValueError(f"Invalid base64 signature: {e}")

        # Construct the message: timestamp + payload
        if not isinstance(timestamp, (bytes, bytearray)):
            timestamp_bytes = timestamp.encode("utf-8")
        else:
            timestamp_bytes = timestamp

        if not isinstance(payload, (bytes, bytearray)):
            payload_bytes = payload.encode("utf-8")
        else:
            payload_bytes = payload

        message = timestamp_bytes + payload_bytes

        # Verify the signature
        try:
            key.verify(signature_bytes, message, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
        except Exception as e:
            # Any other exception is treated as a verification failure
            return False
