class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        if hashAlg is None:
            raise ValueError("hashAlg must not be None")
        if mgf is None:
            raise ValueError("mgf must not be None")

        self.hashAlg = hashAlg
        self.mgf = mgf

        if label is None:
            self.label = b""
        elif isinstance(label, bytes):
            self.label = label
        elif isinstance(label, str):
            self.label = label.encode("utf-8")
        else:
            raise TypeError("label must be bytes, str, or None")

    def to_native(self):
        return {
            "hashAlg": self.hashAlg,
            "mgf": self.mgf,
            "label": self.label,
            "labelLen": len(self.label),
        }
