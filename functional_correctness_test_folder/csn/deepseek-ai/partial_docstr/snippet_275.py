
class Signer:
    '''Abstract base class for signing algorithms.'''

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        raise NotImplementedError("Subclasses must implement this method.")

    def verify(self, msg, sig, key):
        '''Verify the signature ``sig`` for ``msg`` using ``key``.'''
        raise NotImplementedError("Subclasses must implement this method.")
