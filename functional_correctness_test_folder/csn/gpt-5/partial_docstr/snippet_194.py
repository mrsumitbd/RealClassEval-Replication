class EXTRACT_KEY_FROM_KEY_Mechanism:

    def __init__(self, extractParams):
        '''
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        '''
        if isinstance(extractParams, bool) or not isinstance(extractParams, int):
            raise TypeError("extractParams must be an integer (bit index).")
        if extractParams < 0:
            raise ValueError("extractParams must be a non-negative integer.")
        self.extractParams = extractParams

    def to_native(self):
        return self.extractParams
