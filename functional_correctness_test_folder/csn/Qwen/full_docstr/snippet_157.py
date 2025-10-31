
import hashlib


class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        '''Tells the init the original attr.'''
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        if self.original:
            setattr(model_instance, self.name, self.hash_value(self.original))

    def get_placeholder(self, value=None, compiler=None, connection=None):
        '''
        Tell postgres to encrypt this field with a hashing function.
        The `value` string is checked to determine if we need to hash or keep
        the current value.
        `compiler` and `connection` is ignored here as we don't need custom operators.
        '''
        if value and not self.is_hashed(value):
            return self.get_encrypt_sql(connection)
        return '%s'

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return "ENCRYPTBYKEY(KEY_GUID('your_key_name'), %s)"

    def hash_value(self, value):
        '''Hash the given value using SHA-256.'''
        return hashlib.sha256(value.encode()).hexdigest()

    def is_hashed(self, value):
        '''Check if the value is already hashed.'''
        return len(value) == 64 and all(c in '0123456789abcdef' for c in value.lower())
