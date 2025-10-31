
class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.label = label

    def to_native(self):
        mechanism = {
            'hashAlg': self.hashAlg,
            'mgf': self.mgf
        }
        if self.label is not None:
            mechanism['label'] = self.label
        return mechanism
