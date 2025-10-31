
class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        # Store the original value if provided
        self.original = original
        # Allow a key to be passed in kwargs (optional)
        self.key = kwargs.pop('key', None)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        # Retrieve the current value from the instance
        current_value = getattr(model_instance, self.attname)
        # Store it on the instance for later use
        setattr(model_instance, f'_original_{self.attname}', current_value)
        return current_value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        '''Return a SQL placeholder that will encrypt the value using pgcrypto.'''
        # Use the pgp_sym_encrypt function; the key can be a literal or a column name
        if self.key is None:
            # If no key is provided, just return the value placeholder
            return '%s'
        # If the key is a string literal, quote it
        if isinstance(self.key, str) and not self.key.startswith('"'):
            key_sql = f"'{self.key}'"
        else:
            key_sql = self.key
        return f'pgp_sym_encrypt(%s, {key_sql})'

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        # Ensure we are on PostgreSQL
        if connection.vendor != 'postgresql':
            raise NotImplementedError(
                'pgcrypto encryption is only supported on PostgreSQL')
        # Default encryption SQL using pgp_sym_encrypt
        if self.key is None:
            raise ValueError('Encryption key must be provided')
        # Quote the key if it is a literal string
        if isinstance(self.key, str) and not self.key.startswith('"'):
            key_sql = f"'{self.key}'"
        else:
            key_sql = self.key
        return f'pgp_sym_encrypt(%s, {key_sql})'
