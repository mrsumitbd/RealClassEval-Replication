
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib


class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device  # device is expected to have get_private_key(identity) method

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        privkey_bytes = self.device.get_private_key(identity, ecdh=ecdh)
        sk = SigningKey.from_string(privkey_bytes, curve=SECP256k1)
        return sk.get_verifying_key()

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        privkey_bytes = self.device.get_private_key(identity, ecdh=True)
        sk = SigningKey.from_string(privkey_bytes, curve=SECP256k1)
        if isinstance(peer_pubkey, VerifyingKey):
            vk = peer_pubkey
        else:
            vk = VerifyingKey.from_string(peer_pubkey, curve=SECP256k1)
        # ECDH: multiply peer's public point by our private scalar
        shared_point = vk.pubkey.point * sk.privkey.secret_multiplier
        # Use x coordinate as shared secret, hashed
        shared_x = shared_point.x()
        shared_x_bytes = shared_x.to_bytes(32, 'big')
        return hashlib.sha256(shared_x_bytes).digest()
