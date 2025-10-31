
class Client:

    def __init__(self, device):

        self.device = device

    def pubkey(self, identity, ecdh=False):

        if ecdh:
            return self.device.ecdh_pubkey(identity)
        else:
            return self.device.pubkey(identity)

    def ecdh(self, identity, peer_pubkey):

        return self.device.ecdh(identity, peer_pubkey)
