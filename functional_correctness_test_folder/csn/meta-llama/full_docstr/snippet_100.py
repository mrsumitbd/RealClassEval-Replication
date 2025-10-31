
from ecdsa import VerifyingKey, NIST256p
from ecdsa.util import number_to_string
import hashlib


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        pubkey_bytes = self.device.get_pubkey(identity, ecdh)
        return VerifyingKey.from_string(pubkey_bytes, curve=NIST256p, hashfunc=hashlib.sha256)

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        if not isinstance(peer_pubkey, VerifyingKey):
            raise TypeError("peer_pubkey must be a VerifyingKey object")

        peer_pubkey_bytes = peer_pubkey.to_string()
        shared_secret = self.device.ecdh(identity, peer_pubkey_bytes)
        return shared_secret
