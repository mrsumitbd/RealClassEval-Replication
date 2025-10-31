class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        '''
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        '''
        if not isinstance(hashAlg, (int, str)):
            raise TypeError("hashAlg must be int or str")
        if not isinstance(mgf, (int, str)):
            raise TypeError("mgf must be int or str")

        if label is None:
            normalized_label = None
        elif isinstance(label, bytes):
            normalized_label = label
        elif isinstance(label, bytearray):
            normalized_label = bytes(label)
        elif isinstance(label, str):
            normalized_label = label.encode("utf-8")
        else:
            raise TypeError("label must be bytes, bytearray, str, or None")

        self.hash_alg = hashAlg
        self.mgf = mgf
        self.label = normalized_label

    def to_native(self):
        '''convert mechanism to native format'''
        source = "CKZ_DATA_SPECIFIED" if self.label not in (
            None, b"") else "CKZ_NONE"
        return {
            "hashAlg": self.hash_alg,
            "mgf": self.mgf,
            "source": source,
            "label": self.label or b"",
        }
