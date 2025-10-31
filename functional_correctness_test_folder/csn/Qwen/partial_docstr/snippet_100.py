
from ecdsa import SigningKey, VerifyingKey, SECP256k1


class Client:

    def __init__(self, device):
        '''C-tor.'''
        self.device = device
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if ecdh:
            # Assuming identity is a string and we derive a key from it
            derived_key = self.private_key.sign(identity.encode())
            return VerifyingKey.from_string(derived_key, curve=SECP256k1)
        return self.public_key

    def ecdh(self, identity, peer_pubkey):
        # Simple ECDH implementation using the shared secret
        shared_secret = self.private_key.ecdh(peer_pubkey)
        return shared_secret
