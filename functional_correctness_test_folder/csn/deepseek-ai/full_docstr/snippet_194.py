
class EXTRACT_KEY_FROM_KEY_Mechanism:
    '''CKM_EXTRACT_KEY_FROM_KEY key derivation mechanism'''

    def __init__(self, extractParams):
        '''
        :param extractParams: the index of the first bit of the original
        key to be used in the newly-derived key.  For example if
        extractParams=5 then the 5 first bits are skipped and not used.
        '''
        self.extractParams = extractParams

    def to_native(self):
        '''convert mechanism to native format'''
        return {'extractParams': self.extractParams}
