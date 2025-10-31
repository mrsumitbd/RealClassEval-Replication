class RSAOAEPMechanism:
    '''RSA OAEP Wrapping mechanism'''

    def __init__(self, hashAlg, mgf, label=None):
        '''
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        '''
        self.hashAlg = self._coerce_mech(hashAlg, "hashAlg")
        self.mgf = self._coerce_mech(mgf, "mgf")
        self.label = self._coerce_label(label)

    def _coerce_mech(self, value, name):
        if hasattr(value, "value"):
            value = value.value
        try:
            ivalue = int(value)
        except Exception as e:
            raise TypeError(
                f"{name} must be an int or enum-like with 'value'") from e
        if ivalue < 0:
            raise ValueError(f"{name} must be a non-negative integer")
        return ivalue

    def _coerce_label(self, label):
        if label is None:
            return b""
        if isinstance(label, bytes):
            return label
        if isinstance(label, str):
            return label.encode("utf-8")
        try:
            return bytes(label)
        except Exception as e:
            raise TypeError("label must be bytes-like, str, or None") from e

    def to_native(self):
        '''convert mechanism to native format'''
        return {
            "hashAlg": self.hashAlg,
            "mgf": self.mgf,
            "label": self.label,
        }
