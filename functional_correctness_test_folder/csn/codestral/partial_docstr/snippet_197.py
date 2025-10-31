
class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.label = label

    def to_native(self):
        native_mechanism = {
            'hashAlg': self.hashAlg,
            'mgf': self.mgf,
            'label': self.label
        }
        return native_mechanism
