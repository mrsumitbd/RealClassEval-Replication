class Encrypter:
    """Abstract base class for encryption algorithms."""

    def __init__(self, with_digest=False):
        self.with_digest = with_digest

    def encrypt(self, msg, key, **kwargs):
        """Encrypt ``msg`` with ``key`` and return the encrypted message."""
        raise NotImplementedError

    def decrypt(self, msg, key, **kwargs):
        """Return decrypted message."""
        raise NotImplementedError