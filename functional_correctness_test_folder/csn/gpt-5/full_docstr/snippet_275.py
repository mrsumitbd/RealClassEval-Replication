from abc import ABC, abstractmethod


class Signer(ABC):
    '''Abstract base class for signing algorithms.'''

    @abstractmethod
    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        raise NotImplementedError

    @abstractmethod
    def verify(self, msg, sig, key):
        '''Return True if ``sig`` is a valid signature for ``msg``.'''
        raise NotImplementedError
