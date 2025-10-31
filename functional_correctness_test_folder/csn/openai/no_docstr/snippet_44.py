
import base64
import hashlib
from ecdsa import VerifyingKey, SECP256k1, BadSignatureError, util


class EventWebhook:
    """
    Utility class for verifying ECDSA signatures on event payloads.
    """

    def __init__(self, public_key=None):
        """
        Initialize the EventWebhook with an optional public key.

        :param public_key: Public key in hex or base64 string format.
        """
        self.public_key = public_key

    def convert_public_key_to_ecdsa(self, public_key=None):
        """
        Convert a public key string into an ecdsa.VerifyingKey instance.

        The key can be provided in hex or base64 encoding. If no key is
        supplied, the instance's stored public key is used.

        :param public_key: Public key string (hex or base64).
        :return: ecdsa.VerifyingKey instance.
        :raises ValueError: If the key cannot be decoded or is invalid.
        """
        key_str = public_key if public_key is not None else self.public_key
        if key_str is None:
            raise ValueError("No public key provided")

        # Try base64 first
        try:
            key_bytes = base64.b64decode(key_str, validate=True)
        except Exception:
            # Fallback to hex
            try:
                key_bytes = bytes.fromhex(key_str)
            except Exception as exc:
                raise ValueError(
                    "Public key must be base64 or hex encoded") from exc

        try:
            vk = VerifyingKey.from_string(key_bytes, curve=SECP256k1)
        except Exception as exc:
            raise ValueError(
                "Failed to create VerifyingKey from provided public key") from exc

        return vk

    def verify_signature(self, payload, signature, timestamp, public_key=None):
        """
        Verify an ECDSA signature for a given payload and timestamp.

        The signature is expected to be base64 or hex encoded. The message
        that is signed is the concatenation of the timestamp, a dot, and
        the payload (i.e., f"{timestamp}.{payload}").

        :param payload: The event payload (string or bytes).
        :param signature: The signature string (base64 or hex).
        :param timestamp: The timestamp string used in the signed message.
        :param public_key: Optional public key string; if omitted, the
                           instance's stored key is used.
        :return: True if the signature is valid, False otherwise.
        """
        if isinstance(payload, bytes):
            payload_bytes = payload
        else:
            payload_bytes = str(payload).encode("utf-8")

        message = f"{timestamp}.{payload_bytes.decode('utf-8')}".encode(
            "utf-8")
        digest = hashlib.sha256(message).digest()

        # Decode signature
        try:
            sig_bytes = base64.b64decode(signature, validate=True)
        except Exception:
            try:
                sig_bytes = bytes.fromhex(signature)
            except Exception:
                return False

        try:
            vk = self.convert_public_key_to_ecdsa(public_key)
            vk.verify(sig_bytes, digest, sigdecode=util.sigdecode_der)
            return True
        except (BadSignatureError, ValueError):
            return False
