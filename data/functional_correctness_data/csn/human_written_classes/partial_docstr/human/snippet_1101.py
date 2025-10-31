import string
import secrets

class _Key:

    def __init__(self, length: int=32):
        self.length: int = length
        self.persistent: str = ''
        self.__repr__()

    def __repr__(self):
        """Generate a new key, return it and make it persistent"""
        alphabet = string.ascii_letters + string.digits + '#$%&()*+,-./:;<=>?@[]^_~!'
        key = ''.join((secrets.choice(alphabet) for _ in range(self.length)))
        self.persistent = key
        return key

    def __str__(self):
        """Return the persistent key."""
        if not self.persistent:
            return self.__repr__()
        return str(self.persistent)