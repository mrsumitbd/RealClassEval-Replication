class EXTRACT_KEY_FROM_KEY_Mechanism:
    '''CKM_EXTRACT_KEY_FROM_KEY key derivation mechanism'''

    # PKCS#11 constant for CKM_EXTRACT_KEY_FROM_KEY (placeholder value)
    CKM_EXTRACT_KEY_FROM_KEY = 0x00000000

    def __init__(self, extractParams):
        '''
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        '''
        if not isinstance(extractParams, int) or extractParams < 0:
            raise ValueError("extractParams must be a non‑negative integer")
        self.extractParams = extractParams

    def to_native(self):
        '''convert mechanism to native format'''
        # Represent the parameters as a simple dictionary
        params = {'extractParams': self.extractParams}
        # Return a tuple of (mechanism type, parameters)
        return (self.CKM_EXTRACT_KEY_FROM_KEY, params)
