import base64
from typing import Optional, Union

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_der_public_key, load_pem_public_key


class EventWebhook:

    def __init__(self, public_key=None):
        if public_key is None:
            self.public_key = None
        else:
            self.public_key = self.convert_public_key_to_ecdsa(public_key)

    def convert_public_key_to_ecdsa(self, public_key):
        if public_key is None:
            return None

        if isinstance(public_key, ec.EllipticCurvePublicKey):
            return public_key

        key_bytes: Optional[bytes] = None

        if isinstance(public_key, str):
            pem_marker = "-----BEGIN PUBLIC KEY-----" in public_key
            if pem_marker:
                key_bytes = public_key.encode("utf-8")
                try:
                    loaded = load_pem_public_key(key_bytes)
                except Exception as e:
                    raise ValueError("Invalid PEM public key") from e
                if not isinstance(loaded, ec.EllipticCurvePublicKey):
                    raise ValueError(
                        "Public key is not an elliptic curve public key")
                return loaded
            else:
                # Try base64 DER
                try:
                    der = base64.b64decode(public_key)
                    loaded = load_der_public_key(der)
                    if not isinstance(loaded, ec.EllipticCurvePublicKey):
                        raise ValueError(
                            "Public key is not an elliptic curve public key")
                    return loaded
                except Exception:
                    # Try treating as raw bytes string (hex not supported)
                    try:
                        loaded = load_der_public_key(
                            public_key.encode("utf-8"))
                        if not isinstance(loaded, ec.EllipticCurvePublicKey):
                            raise ValueError(
                                "Public key is not an elliptic curve public key")
                        return loaded
                    except Exception as e:
                        raise ValueError(
                            "Unable to load public key from provided string") from e

        if isinstance(public_key, (bytes, bytearray)):
            # Try PEM first
            try:
                loaded = load_pem_public_key(public_key)
                if isinstance(loaded, ec.EllipticCurvePublicKey):
                    return loaded
            except Exception:
                pass
            # Then DER
            try:
                loaded = load_der_public_key(public_key)
                if isinstance(loaded, ec.EllipticCurvePublicKey):
                    return loaded
            except Exception as e:
                raise ValueError("Unable to load public key from bytes") from e

        raise ValueError("Unsupported public_key type")

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
        key_obj: Optional[ec.EllipticCurvePublicKey]

        if public_key is not None:
            key_obj = self.convert_public_key_to_ecdsa(public_key)
        else:
            if self.public_key is None:
                raise ValueError("Public key is required to verify signature")
            key_obj = self.public_key

        if isinstance(payload, str):
            payload_bytes = payload.encode("utf-8")
        elif isinstance(payload, (bytes, bytearray)):
            payload_bytes = bytes(payload)
        else:
            raise ValueError("payload must be str or bytes")

        if isinstance(timestamp, (bytes, bytearray)):
            timestamp_str = bytes(timestamp).decode("utf-8")
        else:
            timestamp_str = str(timestamp)

        message = (timestamp_str.encode("utf-8") + payload_bytes)

        if isinstance(signature, str):
            try:
                signature_bytes = base64.b64decode(signature, validate=True)
            except Exception:
                # Some environments may send URL-safe base64
                try:
                    signature_bytes = base64.urlsafe_b64decode(signature)
                except Exception as e:
                    raise ValueError("Invalid signature encoding") from e
        elif isinstance(signature, (bytes, bytearray)):
            signature_bytes = bytes(signature)
        else:
            raise ValueError("signature must be str or bytes")

        try:
            key_obj.verify(signature_bytes, message, ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False
