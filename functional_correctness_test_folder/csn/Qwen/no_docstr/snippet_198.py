
class RSA_PSS_Mechanism:

    def __init__(self, mecha, hashAlg, mgf, sLen):
        self.mecha = mecha
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.sLen = sLen

    def to_native(self):
        return {
            'mecha': self.mecha,
            'hashAlg': self.hashAlg,
            'mgf': self.mgf,
            'sLen': self.sLen
        }
