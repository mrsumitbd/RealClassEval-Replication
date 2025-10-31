
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend


class Client:

    def __init__(self, device):
        '''C-tor.'''
        self.device = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if ecdh:
            private_key = ec.generate_private_key(
                ec.SECP256R1(), default_backend())
            self.device.store_private_key(identity, private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            return private_key.public_key()
        else:
            return self.device.get_public_key(identity)

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH.'''
        private_key_bytes = self.device.get_private_key(identity)
        if private_key_bytes is None:
            raise ValueError("Private key not found")

        private_key = serialization.load_der_private_key(
            private_key_bytes,
            password=None,
            backend=default_backend()
        )

        peer_public_key = serialization.load_der_public_key(
            peer_pubkey.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ),
            backend=default_backend()
        )

        shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
        return shared_secret
