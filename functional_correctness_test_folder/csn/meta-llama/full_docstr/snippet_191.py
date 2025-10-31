
from ctypes import c_ulong, c_void_p, c_ubyte, sizeof, Structure


class CK_GCM_PARAMS(Structure):
    _fields_ = [
        ("pIv", c_void_p),
        ("ulIvLen", c_ulong),
        ("pAAD", c_void_p),
        ("ulAADLen", c_ulong),
        ("ulTagBits", c_ulong)
    ]


class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    def __init__(self, iv, aad, tagBits):
        '''
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        '''
        self.iv = iv
        self.aad = aad
        self.tagBits = tagBits

    def to_native(self):
        '''convert mechanism to native format'''
        gcm_params = CK_GCM_PARAMS()
        gcm_params.pIv = (c_ubyte * len(self.iv))(*self.iv)
        gcm_params.ulIvLen = len(self.iv)
        gcm_params.pAAD = (c_ubyte * len(self.aad))(*self.aad)
        gcm_params.ulAADLen = len(self.aad)
        gcm_params.ulTagBits = self.tagBits

        mechanism = (c_ulong * 3)()
        mechanism[0] = 0x000001087  # CKM_AES_GCM
        mechanism[1] = c_void_p(ctypes.addressof(gcm_params))
        mechanism[2] = sizeof(gcm_params)

        return mechanism
