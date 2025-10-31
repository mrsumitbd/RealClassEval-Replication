
class Signer:
    '''Abstract base class for signing algorithms.'''

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        pass

    def verify(self, msg, sig, key):
        '''Verify ``msg`` with ``sig`` using ``key`` and return the result.'''
        pass
