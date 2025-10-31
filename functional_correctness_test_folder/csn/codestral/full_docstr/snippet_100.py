
class Client:
    '''Sign messages and get public keys from a hardware device.'''

    def __init__(self, device):
        '''C-tor.'''
        self.device = device

    def pubkey(self, identity, ecdh=False):
        '''Return public key as VerifyingKey object.'''
        if ecdh:
            return self.device.get_ecdh_pubkey(identity)
        else:
            return self.device.get_pubkey(identity)

    def ecdh(self, identity, peer_pubkey):
        '''Derive shared secret using ECDH from peer public key.'''
        return self.device.ecdh(identity, peer_pubkey)
