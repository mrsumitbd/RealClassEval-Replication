
from ctypes import c_ulong, c_void_p, cast, POINTER


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
        self.label = label

    def to_native(self):
        '''convert mechanism to native format'''
        from ctypes import sizeof, c_char, create_string_buffer
        from .pkcs11constants import CKM_RSA_PKCS_OAEP, CK_RSA_PKCS_OAEP_PARAMS, CK_MECHANISM

        params = CK_RSA_PKCS_OAEP_PARAMS()
        params.hashAlg = self.hashAlg
        params.mgf = self.mgf
        params.source = 0  # CKZ_DATA_SPECIFIED
        if self.label is not None:
            label_len = len(self.label)
            params.pSourceData = cast(create_string_buffer(
                self.label.encode('utf-8')), c_void_p)
            params.ulSourceDataLen = label_len
        else:
            params.pSourceData = None
            params.ulSourceDataLen = 0

        mechanism = CK_MECHANISM()
        mechanism.mechanism = CKM_RSA_PKCS_OAEP
        mechanism.pParameter = cast(
            cast(addressof(params), POINTER(c_char)), c_void_p)
        mechanism.ulParameterLen = c_ulong(sizeof(params))

        return mechanism
