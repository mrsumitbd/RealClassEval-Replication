
import hashlib


class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original_value = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        if hasattr(model_instance, 'original_value'):
            model_instance.original_value = self.original_value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if value is None:
            return '%s'
        return hashlib.sha256(str(value).encode()).hexdigest()

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return "pgp_sym_encrypt(%s, %s)"
