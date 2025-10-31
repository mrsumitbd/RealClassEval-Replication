import string

class Constants:

    @classmethod
    def values(cls):
        for key, value in cls.__dict__.items():
            if not key.startswith('_'):
                yield value

    @classmethod
    def str(cls, value):
        """Convert status (id) to its string name."""
        for k, v in cls.__dict__.items():
            if k[0] in string.ascii_uppercase and v == value:
                return k.lower().replace('_', ' ')