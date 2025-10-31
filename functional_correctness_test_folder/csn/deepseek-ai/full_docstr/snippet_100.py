
from ecdsa import VerifyingKey, NIST256p, SigningKey
import hashlib


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device
        self._private_keys = {}

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if identity not in self._private_keys:
            self._private_keys[identity] = SigningKey.generate(curve=NIST256p)
        private_key = self._private_keys[identity]
        return private_key.get_verifying_key()

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        if identity not in self._private_keys:
            self._private_keys[identity] = SigningKey.generate(curve=NIST256p)
        private_key = self._private_keys[identity]
        shared_secret = private_key.privkey.secret_multiplier * peer_pubkey.pubkey.point
        return hashlib.sha256(str(shared_secret).encode()).digest()
