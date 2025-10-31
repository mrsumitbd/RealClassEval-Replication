
import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class Client:
    """
    A simple client that manages a set of elliptic‑curve key pairs
    and can perform ECDH key exchange with a peer.
    """

    def __init__(self, device=None):
        """
        Initialise the client with an optional device.

        Parameters
        ----------
        device : dict, optional
            A mapping from identity strings to private keys. If not
            provided, an empty dictionary is created.
        """
        self._device = device if device is not None else {}

    def pubkey(self, identity, ecdh=False):
        """
        Return the public key for the given identity. If the identity
        does not yet have a key pair, one is generated.

        Parameters
        ----------
        identity : str
            The identifier for the key pair.
        ecdh : bool, optional
            Ignored in this implementation but kept for API compatibility.

        Returns
        -------
        bytes
            The public key encoded in PEM format.
        """
        if identity not in self._device:
            # Generate a new private key for this identity
            private_key = ec.generate_private_key(ec.SECP256R1())
            self._device[identity] = private_key
        else:
            private_key = self._device[identity]

        public_key = private_key.public_key()
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return pem

    def ecdh(self, identity, peer_pubkey):
        """
        Perform an ECDH key exchange with a peer public key.

        Parameters
        ----------
        identity : str
            The identifier for the local key pair.
        peer_pubkey : bytes
            The peer's public key in PEM format.

        Returns
        -------
        bytes
            A derived shared secret (32 bytes) using HKDF.
        """
        if identity not in self._device:
            raise ValueError(f"Identity '{identity}' not found in device.")

        private_key = self._device[identity]

        # Load the peer's public key
        peer_public_key = serialization.load_pem_public_key(peer_pubkey)

        # Perform raw ECDH to get the shared secret
        shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)

        # Derive a fixed‑size key from the shared secret
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"ecdh shared secret",
        ).derive(shared_secret)

        return derived_key
