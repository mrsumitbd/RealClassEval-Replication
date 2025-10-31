
from ctypes import c_ulong, c_void_p, cast, POINTER, sizeof


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
        self.label = label

    def to_native(self):
        '''convert mechanism to native format'''
        from ctypes import create_string_buffer
        from pkcs11.constants import CKM_RSA_PKCS_OAEP, CKO_DATA
        from pkcs11.types import CK_RSA_PKCS_OAEP_PARAMS, CK_MECHANISM, CK_MECHANISM_TYPE, CK_OBJECT_CLASS

        params = CK_RSA_PKCS_OAEP_PARAMS()
        params.hashAlg = self.hashAlg
        params.mgf = self.mgf
        params.source = CKO_DATA  # hardcoded, as per PKCS#11 v2.40
        if self.label is None:
            params.pSourceData = None
            params.ulSourceDataLen = 0
        else:
            label_buf = create_string_buffer(self.label.encode())
            params.pSourceData = cast(label_buf, c_void_p)
            params.ulSourceDataLen = len(self.label)

        mechanism = CK_MECHANISM()
        mechanism.mechanism = CKM_RSA_PKCS_OAEP
        mechanism.pParameter = cast(c_void_p(id(params)), POINTER(c_void_p))
        mechanism.ulParameterLen = sizeof(params)

        return mechanism
