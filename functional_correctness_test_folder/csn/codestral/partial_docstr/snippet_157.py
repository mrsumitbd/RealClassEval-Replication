
class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original = original

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        if self.original is not None:
            setattr(model_instance, self.attname, self.original)

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if value is None:
            value = self.value_from_object(self.model)
        if value is None:
            return 'NULL'
        if connection is None:
            connection = compiler.connection
        return self.get_encrypt_sql(connection) % self.get_db_prep_value(value, connection=connection)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return "pgp_sym_encrypt(%s, '%s')" % (connection.ops.placeholder, self.key)
