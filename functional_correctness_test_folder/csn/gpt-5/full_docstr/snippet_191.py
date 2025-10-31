class AES_GCM_Mechanism:
    '''CKM_AES_GCM warpping mechanism'''

    import ctypes as _ctypes

    class _CK_GCM_PARAMS(_ctypes.Structure):
        _fields_ = [
            ('pIv', _ctypes.c_void_p),
            ('ulIvLen', _ctypes.c_ulong),
            ('pAAD', _ctypes.c_void_p),
            ('ulAADLen', _ctypes.c_ulong),
            ('ulTagBits', _ctypes.c_ulong),
        ]

    def __init__(self, iv, aad, tagBits):
        '''
        :param iv: initialization vector
        :param aad: additional authentication data
        :param tagBits: length of authentication tag in bits
        '''
        # Normalize inputs
        if iv is None:
            iv_bytes = b""
        else:
            try:
                iv_bytes = bytes(iv)
            except Exception as e:
                raise TypeError("iv must be bytes-like or None") from e

        if aad is None:
            aad_bytes = b""
        else:
            try:
                aad_bytes = bytes(aad)
            except Exception as e:
                raise TypeError("aad must be bytes-like or None") from e

        if not isinstance(tagBits, int) or tagBits < 0:
            raise ValueError("tagBits must be a non-negative integer")

        # Keep original for reference
        self.iv = iv_bytes
        self.aad = aad_bytes
        self.tagBits = int(tagBits)

        # Prepare native buffers and structure; keep buffers alive on the instance
        self._iv_buf = (self._ctypes.c_ubyte * len(iv_bytes)
                        )(*iv_bytes) if iv_bytes else None
        self._aad_buf = (self._ctypes.c_ubyte * len(aad_bytes)
                         )(*aad_bytes) if aad_bytes else None

        pIv = self._ctypes.cast(
            self._iv_buf, self._ctypes.c_void_p) if self._iv_buf is not None else self._ctypes.c_void_p()
        pAAD = self._ctypes.cast(
            self._aad_buf, self._ctypes.c_void_p) if self._aad_buf is not None else self._ctypes.c_void_p()

        self._params = self._CK_GCM_PARAMS(
            pIv=pIv,
            ulIvLen=len(iv_bytes),
            pAAD=pAAD,
            ulAADLen=len(aad_bytes),
            ulTagBits=self.tagBits,
        )

    def to_native(self):
        '''convert mechanism to native format'''
        return self._params
