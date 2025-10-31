class EXTRACT_KEY_FROM_KEY_Mechanism:
    '''CKM_EXTRACT_KEY_FROM_KEY key derivation mechanism'''

    def __init__(self, extractParams):
        '''
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        '''
        if not isinstance(extractParams, int):
            raise TypeError("extractParams must be an integer")
        if extractParams < 0:
            raise ValueError("extractParams must be non-negative")
        self.extractParams = extractParams

    def to_native(self):
        '''convert mechanism to native format'''
        import struct
        import ctypes

        size = ctypes.sizeof(ctypes.c_ulong)
        if size == 4:
            fmt = "=L"
            max_val = (1 << 32) - 1
        elif size == 8:
            fmt = "=Q"
            max_val = (1 << 64) - 1
        else:
            raise RuntimeError("Unsupported c_ulong size")

        if self.extractParams > max_val:
            raise OverflowError("extractParams too large for native CK_ULONG")

        return struct.pack(fmt, self.extractParams)
