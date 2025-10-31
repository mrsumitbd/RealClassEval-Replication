
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
        if self.original is not None:
            setattr(model_instance, self.original,
                    getattr(model_instance, self.attname))

    def get_placeholder(self, value=None, compiler=None, connection=None):
        '''
        Tell postgres to encrypt this field with a hashing function.
        The `value` string is checked to determine if we need to hash or keep
        the current value.
        `compiler` and `connection` is ignored here as we don't need custom operators.
        '''
        if value is None or value == '':
            return '%s'
        return f"crypt(%s, gen_salt('bf'))"

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return "crypt(%s, gen_salt('bf'))"
