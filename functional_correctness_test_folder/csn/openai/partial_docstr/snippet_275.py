
from abc import ABC, abstractmethod


class Signer(ABC):
    '''Abstract base class for signing algorithms.'''

    @abstractmethod
    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        pass

    @abstractmethod
    def verify(self, msg, sig, key):
        '''Verify ``sig`` for ``msg`` using ``key``. Return True if valid.'''
        pass
