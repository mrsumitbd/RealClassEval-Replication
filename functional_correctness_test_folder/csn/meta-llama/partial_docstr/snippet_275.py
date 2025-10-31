
from abc import ABC, abstractmethod
import hashlib
import hmac


class Signer(ABC):
    '''Abstract base class for signing algorithms.'''

    @abstractmethod
    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        pass

    @abstractmethod
    def verify(self, msg, sig, key):
        '''Verify that ``sig`` is a valid signature for ``msg`` with ``key``.'''
        pass


class HMACSigner(Signer):
    def __init__(self, hash_algorithm=hashlib.sha256):
        self.hash_algorithm = hash_algorithm

    def sign(self, msg, key):
        return hmac.new(key, msg, self.hash_algorithm).digest()

    def verify(self, msg, sig, key):
        expected_sig = self.sign(msg, key)
        return hmac.compare_digest(sig, expected_sig)


class SimpleSigner(Signer):
    def sign(self, msg, key):
        # Simple signing algorithm for demonstration purposes only.
        # In a real application, use a secure signing algorithm like HMAC.
        return bytes([x ^ key for x in msg])

    def verify(self, msg, sig, key):
        expected_sig = self.sign(msg, key)
        return sig == expected_sig


# Example usage:
if __name__ == "__main__":
    msg = b"Hello, world!"
    key = b"secret_key"

    hmac_signer = HMACSigner()
    sig = hmac_signer.sign(msg, key)
    print("HMAC Signature:", sig.hex())
    print("HMAC Verification:", hmac_signer.verify(msg, sig, key))

    simple_signer = SimpleSigner()
    key = 0x12  # SimpleSigner uses an integer key for XOR operation
    sig = simple_signer.sign(msg, key)
    print("Simple Signature:", sig.hex())
    print("Simple Verification:", simple_signer.verify(msg, sig, key))
