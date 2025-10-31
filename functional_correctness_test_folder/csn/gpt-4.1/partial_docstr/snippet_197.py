
class RSAOAEPMechanism:

    def __init__(self, hashAlg, mgf, label=None):
        '''
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        '''
        self.hashAlg = hashAlg
        self.mgf = mgf
        if label is not None:
            if isinstance(label, str):
                self.label = label.encode('utf-8')
            else:
                self.label = label
        else:
            self.label = None

    def to_native(self):
        '''convert mechanism to native format'''
        native = {
            'hashAlg': self.hashAlg,
            'mgf': self.mgf,
            'label': self.label if self.label is not None else b''
        }
        return native
