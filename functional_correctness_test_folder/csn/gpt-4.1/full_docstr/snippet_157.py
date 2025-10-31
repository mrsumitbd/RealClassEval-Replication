
class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        '''Tells the init the original attr.'''
        self.original = original
        self.original_value = None
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        if self.original:
            self.original_value = getattr(model_instance, self.original, None)

    def get_placeholder(self, value=None, compiler=None, connection=None):
        '''
        Tell postgres to encrypt this field with a hashing function.
        The `value` string is checked to determine if we need to hash or keep
        the current value.
        `compiler` and `connection` is ignored here as we don't need custom operators.
        '''
        if value is not None and isinstance(value, str) and value.startswith('hash:'):
            # Already hashed, keep as is
            return '%s'
        else:
            # Hash using pgcrypto's digest function (e.g., SHA256)
            return self.get_encrypt_sql(connection)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        # Default to SHA256 hash using pgcrypto's digest function
        return "digest(%s, 'sha256')"
