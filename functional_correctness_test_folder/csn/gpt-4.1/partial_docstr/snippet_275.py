
class Signer:
    '''Abstract base class for signing algorithms.'''

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        raise NotImplementedError("sign() must be implemented by subclasses.")

    def verify(self, msg, sig, key):
        '''Verify that ``sig`` is a valid signature for ``msg`` with ``key``.'''
        raise NotImplementedError(
            "verify() must be implemented by subclasses.")
