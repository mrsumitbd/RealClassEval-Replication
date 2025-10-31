
class Signer:
    '''Abstract base class for signing algorithms.'''

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        raise NotImplementedError("Subclasses should implement this method.")

    def verify(self, msg, sig, key):
        raise NotImplementedError("Subclasses should implement this method.")
