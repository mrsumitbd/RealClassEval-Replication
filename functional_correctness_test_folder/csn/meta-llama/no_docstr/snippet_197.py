
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        self.hashAlg = hashAlg
        self.mgf = mgf
        self.label = label

    def to_native(self):
        hash_alg = getattr(hashes, self.hashAlg.upper())()
        mgf = padding.MGF1(algorithm=hash_alg)
        if self.label is None:
            return padding.OAEP(
                mgf=mgf,
                algorithm=hash_alg,
                label=None
            )
        else:
            return padding.OAEP(
                mgf=mgf,
                algorithm=hash_alg,
                label=self.label
            )
