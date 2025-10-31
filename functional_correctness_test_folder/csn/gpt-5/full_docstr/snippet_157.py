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
        # Determine which attribute to read plaintext from
        if self.original:
            value = getattr(model_instance, self.original, None)
            # Ensure the database receives the plaintext for hashing
            setattr(model_instance, self.attname, value)
        else:
            value = getattr(model_instance, self.attname, None)

        # Keep a reference to the value used for hashing during this save
        setattr(model_instance, f'_{self.attname}_original_value', value)
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        '''
        Tell postgres to encrypt this field with a hashing function.
        The `value` string is checked to determine if we need to hash or keep
        the current value.
        `compiler` and `connection` is ignored here as we don't need custom operators.
        '''
        # If no value is provided, keep the placeholder as-is
        if value is None:
            return "%s"
        # Always hash non-null values
        return self.get_encrypt_sql(connection)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        # Store hex-encoded SHA-256 digest of the input using pgcrypto
        return "encode(digest(%s, 'sha256'), 'hex')"
