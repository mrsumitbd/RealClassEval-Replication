
import hashlib
import hmac


class Signer:
    '''Abstract base class for signing algorithms.'''

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        pass

    def verify(self, msg, sig, key):
        '''Return True if ``sig`` is a valid signature for ``msg``.'''
        pass


class HMACSigner(Signer):
    '''Concrete implementation of Signer using HMAC.'''

    def __init__(self, hash_algorithm=hashlib.sha256):
        '''
        Initialize the HMACSigner.

        :param hash_algorithm: The hash algorithm to use for HMAC.
        '''
        self.hash_algorithm = hash_algorithm

    def sign(self, msg, key):
        '''Sign ``msg`` with ``key`` and return the signature.'''
        return hmac.new(key, msg, self.hash_algorithm).digest()

    def verify(self, msg, sig, key):
        '''Return True if ``sig`` is a valid signature for ``msg``.'''
        expected_sig = self.sign(msg, key)
        return hmac.compare_digest(sig, expected_sig)


# Example usage:
if __name__ == "__main__":
    signer = HMACSigner()

    key = b"secret_key"
    msg = b"Hello, World!"
    sig = signer.sign(msg, key)

    print(f"Signature: {sig.hex()}")

    is_valid = signer.verify(msg, sig, key)
    print(f"Is signature valid? {is_valid}")

    # Test with invalid signature
    is_valid = signer.verify(msg, b"invalid_signature", key)
    print(f"Is invalid signature valid? {is_valid}")
