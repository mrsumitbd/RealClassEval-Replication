
import ctypes

# PKCS#11 mechanism type for AES GCM
CKM_AES_GCM = 0x0000010C


class CK_AES_GCM_PARAMS(ctypes.Structure):
    _fields_ = [
        ("pIv", ctypes.c_void_p),      # pointer to IV
        ("ulIvLen", ctypes.c_ulong),   # length of IV
        ("pAAD", ctypes.c_void_p),     # pointer to AAD
        ("ulAADLen", ctypes.c_ulong),  # length of AAD
        ("ulTagBits", ctypes.c_ulong),  # tag length in bits
    ]


class AES_GCM_Mechanism:
    '''CKM_AES_GCM wrapping mechanism'''

    def __init__(self, iv, aad, tagBits):
        """
        :param iv: initialization vector (bytes-like)
        :param aad: additional authentication data (bytes-like)
        :param tagBits: length of authentication tag in bits (int)
        """
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes or bytearray")
        if not isinstance(aad, (bytes, bytearray)):
            raise TypeError("aad must be bytes or bytearray")
        if not isinstance(tagBits, int):
            raise TypeError("tagBits must be an integer")
        if tagBits % 8 != 0:
            raise ValueError("tagBits must be a multiple of 8")

        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = tagBits

        # Allocate buffers for IV and AAD
        self._iv_buf = ctypes.create_string_buffer(self.iv)
        self._aad_buf = ctypes.create_string_buffer(self.aad)

        # Prepare the native parameters structure
        self._params = CK_AES_GCM_PARAMS(
            pIv=ctypes.cast(self._iv_buf, ctypes.c_void_p),
            ulIvLen=ctypes.c_ulong(len(self.iv)),
            pAAD=ctypes.cast(self._aad_buf, ctypes.c_void_p),
            ulAADLen=ctypes.c_ulong(len(self.aad)),
            ulTagBits=ctypes.c_ulong(self.tagBits)
        )

    def to_native(self):
        """
        Convert mechanism to native format.

        Returns:
            tuple: (mechanism_type, params_struct)
        """
        return (CKM_AES_GCM, self._params)
