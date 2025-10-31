
class Client:

    def __init__(self, device):
        self.device = device

    def pubkey(self, identity, ecdh=False):
        if ecdh:
            return self.device.generate_ecdh_pubkey(identity)
        else:
            return self.device.generate_pubkey(identity)

    def ecdh(self, identity, peer_pubkey):
        return self.device.perform_ecdh(identity, peer_pubkey)
