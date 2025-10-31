
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey, PublicKey, Box


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if ecdh:
            return PublicKey(self.device.get_ecdh_public_key(identity))
        else:
            return VerifyKey(self.device.get_signing_public_key(identity))

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        private_key = PrivateKey(self.device.get_ecdh_private_key(identity))
        peer_public_key = PublicKey(peer_pubkey)
        box = Box(private_key, peer_public_key)
        return box.shared_key
