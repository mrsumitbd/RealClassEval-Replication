
import ctypes

# PKCS#11 constants (partial)
CKM_AES_GCM = 0x0000100C


class CK_AES_GCM_PARAMS(ctypes.Structure):
    _fields_ = [
        ("pIv", ctypes.c_void_p),
        ("ulIvLen", ctypes.c_ulong),
        ("pAAD", ctypes.c_void_p),
        ("ulAADLen", ctypes.c_ulong),
        ("ulTagBits", ctypes.c_ulong),
    ]


class CK_MECHANISM(ctypes.Structure):
    _fields_ = [
        ("mechanism", ctypes.c_ulong),
        ("pParameter", ctypes.c_void_p),
        ("ulParameterLen", ctypes.c_ulong),
    ]


class AES_GCM_Mechanism:
    '''CKM_AES_GCM wrapping mechanism'''

    def __init__(self, iv, aad, tagBits):
        """
        Parameters
        ----------
        iv : bytes or bytearray
            Initialization vector.
        aad : bytes or bytearray
            Additional authenticated data.
        tagBits : int
            Length of the authentication tag in bits.
        """
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes or bytearray")
        if not isinstance(aad, (bytes, bytearray)):
            raise TypeError("aad must be bytes or bytearray")
        if not isinstance(tagBits, int) or tagBits <= 0:
            raise ValueError("tagBits must be a positive integer")

        self.iv = bytes(iv)
        self.aad = bytes(aad)
        self.tagBits = tagBits

        # Keep references to the ctypes buffers so they stay alive
        self._iv_buf = (ctypes.c_ubyte * len(self.iv))(*self.iv)
        self._aad_buf = (ctypes.c_ubyte * len(self.aad))(*self.aad)

    def to_native(self):
        """
        Convert the mechanism to a native CK_MECHANISM structure.

        Returns
        -------
        CK_MECHANISM
            A ctypes structure ready to be passed to PKCS#11 functions.
        """
        params = CK_AES_GCM_PARAMS(
            pIv=ctypes.cast(self._iv_buf, ctypes.c_void_p),
            ulIvLen=len(self.iv),
            pAAD=ctypes.cast(self._aad_buf, ctypes.c_void_p),
            ulAADLen=len(self.aad),
            ulTagBits=self.tagBits,
        )

        mech = CK_MECHANISM(
            mechanism=CKM_AES_GCM,
            pParameter=ctypes.cast(ctypes.pointer(params), ctypes.c_void_p),
            ulParameterLen=ctypes.sizeof(params),
        )
        # Store params to keep it alive
        self._params = params
        return mech
