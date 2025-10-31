
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class Client:
    def __init__(self, device):
        self.device = device
        self._keys = {}  # identity -> (private_key, public_key)
        self._ecdh_keys = {}  # identity -> (private_key, public_key)

    def pubkey(self, identity, ecdh=False):
        if not ecdh:
            if identity not in self._keys:
                private_key = ec.generate_private_key(ec.SECP256R1())
                public_key = private_key.public_key()
                self._keys[identity] = (private_key, public_key)
            else:
                private_key, public_key = self._keys[identity]
        else:
            if identity not in self._ecdh_keys:
                private_key = ec.generate_private_key(ec.SECP256R1())
                public_key = private_key.public_key()
                self._ecdh_keys[identity] = (private_key, public_key)
            else:
                private_key, public_key = self._ecdh_keys[identity]
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def ecdh(self, identity, peer_pubkey):
        if identity not in self._ecdh_keys:
            raise ValueError(
                "No ECDH key for this identity. Call pubkey(identity, ecdh=True) first.")
        private_key, _ = self._ecdh_keys[identity]
        peer_public_key = serialization.load_pem_public_key(peer_pubkey)
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        # Derive a key from the shared secret
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'ecdh handshake',
        ).derive(shared_key)
        return derived_key
