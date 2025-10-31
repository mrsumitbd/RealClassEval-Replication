
class EXTRACT_KEY_FROM_KEY_Mechanism:
    '''CKM_EXTRACT_KEY_FROM_KEY key derivation mechanism'''

    def __init__(self, extractParams):
        '''
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        '''
        if not isinstance(extractParams, int) or extractParams < 0:
            raise ValueError("extractParams must be a non-negative integer")
        self.extractParams = extractParams

    def to_native(self):
        '''convert mechanism to native format'''
        # Simulate a native structure as a tuple (mechanism, params)
        CKM_EXTRACT_KEY_FROM_KEY = 0x00000365  # Example PKCS#11 mechanism value
        # The native format would typically be a tuple or a dict
        return (CKM_EXTRACT_KEY_FROM_KEY, self.extractParams)
