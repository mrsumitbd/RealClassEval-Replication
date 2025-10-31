
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


class Client:

    def __init__(self, device):
        '''C-tor.'''
        self.device = device
        self._keys = {}

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if identity not in self._keys:
            if ecdh:
                private_key = ec.generate_private_key(ec.SECP256R1())
            else:
                private_key = ec.generate_private_key(ec.SECP256R1())
            self._keys[identity] = private_key
        public_key = self._keys[identity].public_key()
        return public_key

    def ecdh(self, identity, peer_pubkey):
        if identity not in self._keys:
            raise ValueError("No such identity")
        private_key = self._keys[identity]
        shared_key = private_key.exchange(ec.ECDH(), peer_pubkey)
        return shared_key
