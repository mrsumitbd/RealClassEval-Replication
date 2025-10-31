class HashMixin:
    """Keyed hash mixin.

    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    """
    encrypt_sql = None

    def __init__(self, original=None, *args, **kwargs):
        """Tells the init the original attr."""
        self.original = original
        super(HashMixin, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """Save the original_value."""
        if self.original:
            original_value = getattr(model_instance, self.original)
            setattr(model_instance, self.attname, original_value)
        return super(HashMixin, self).pre_save(model_instance, add)

    def get_placeholder(self, value=None, compiler=None, connection=None):
        """
        Tell postgres to encrypt this field with a hashing function.

        The `value` string is checked to determine if we need to hash or keep
        the current value.

        `compiler` and `connection` is ignored here as we don't need custom operators.
        """
        if value is None or value.startswith('\\x'):
            return '%s'
        return self.get_encrypt_sql(connection)

    def get_encrypt_sql(self, connection):
        """Get encrypt sql. This may be overidden by some implementations."""
        return self.encrypt_sql