class Signer:

    def __init__(self, cert, sig, tosign):
        self.cert = cert
        self.sig = sig
        self.tosign = tosign
        self.mech = None

    def certificate(self):
        return (1, self.cert)

    def sign(self, keyid, data, mech):
        if self.tosign:
            assert self.tosign == data
        self.tosign = data
        self.mech = mech
        if self.sig is None:
            sig = None
            if mech == 'sha256':
                sig = b'\x00' * 256
            return sig
        return self.sig