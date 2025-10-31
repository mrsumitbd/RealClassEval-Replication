
class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original = original

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        if hasattr(model_instance, 'original_value'):
            setattr(model_instance, 'original_value', self.original)
        else:
            model_instance.original_value = self.original
        return self.original

    def get_placeholder(self, value=None, compiler=None, connection=None):
        return self.get_encrypt_sql(connection)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        # Default: use pgcrypto's digest function for SHA256
        return "digest(%s, 'sha256')"
