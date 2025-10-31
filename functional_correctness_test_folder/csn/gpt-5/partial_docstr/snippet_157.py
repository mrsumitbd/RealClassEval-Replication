class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original = original or 'original_value'
        self.algorithm = kwargs.pop('algorithm', 'sha256')
        self.key = kwargs.pop('key', None)
        # Allow SECRET_KEY fallback if Django settings are available.
        if self.key is None:
            try:
                from django.conf import settings
                self.key = getattr(settings, 'SECRET_KEY', '')
            except Exception:
                self.key = ''
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        # Attempt to fetch the raw/original value from the instance using the field's attname
        value = None
        attname = getattr(self, 'attname', None)
        if attname:
            value = getattr(model_instance, attname, None)
        # Store original value on the model instance if configured
        if self.original:
            try:
                setattr(model_instance, self.original, value)
            except Exception:
                pass
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        placeholder = '%s'
        if connection is not None:
            try:
                placeholder = connection.ops.placeholder(value)
            except Exception:
                placeholder = '%s'
        # Return a PostgreSQL expression that computes a keyed hash using pgcrypto's hmac()
        return self.get_encrypt_sql(connection).format(placeholder=placeholder)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        # Safely inline the key and algorithm as SQL string literals
        key = self.key or ''
        algo = self.algorithm or 'sha256'
        key_sql = "'" + key.replace("'", "''") + "'"
        algo_sql = "'" + algo.replace("'", "''") + "'"
        # Use a format placeholder for the parameter placeholder to be supplied by get_placeholder
        # hmac(data bytea, key text, type text) returns bytea
        return f"hmac({{placeholder}}::bytea, {key_sql}, {algo_sql})"
