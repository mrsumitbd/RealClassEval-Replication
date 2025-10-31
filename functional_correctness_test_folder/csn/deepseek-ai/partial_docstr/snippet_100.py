
from ecdsa import VerifyingKey, NIST256p, SigningKey
import hashlib


class Client:

    def __init__(self, device):
        '''C-tor.'''
        self.device = device
        self._private_key = SigningKey.generate(curve=NIST256p)

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        return self._private_key.get_verifying_key()

    def ecdh(self, identity, peer_pubkey):
        shared_secret = self._private_key.privkey.secret_multiplier * peer_pubkey.pubkey.point
        return hashlib.sha256(str(shared_secret).encode()).digest()
