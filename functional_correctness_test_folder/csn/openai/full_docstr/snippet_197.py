
class RSAOAEPMechanism:
    '''RSA OAEP Wrapping mechanism'''

    def __init__(self, hashAlg, mgf, label=None):
        '''
        :param hashAlg: the hash algorithm to use (like `CKM_SHA256`)
        :param mgf: the mask generation function to use (like
          `CKG_MGF1_SHA256`)
        :param label: the (optional) label to use
        '''
        self.hashAlg = hashAlg
        self.mgf = mgf
        if label is None:
            self.label = None
        else:
            if isinstance(label, str):
                self.label = label.encode()
            else:
                self.label = bytes(label)

    def to_native(self):
        '''convert mechanism to native format'''
        from PyKCS11.LowLevel import CK_RSA_PKCS_OAEP_PARAMS, CKM_RSA_PKCS_OAEP
        params = CK_RSA_PKCS_OAEP_PARAMS()
        params.hashAlg = self.hashAlg
        params.mgf = self.mgf
        if self.label is None:
            params.pLabel = None
            params.ulLabelLen = 0
        else:
            params.pLabel = self.label
            params.ulLabelLen = len(self.label)
        return (CKM_RSA_PKCS_OAEP, params)
