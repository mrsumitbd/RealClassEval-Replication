
import psycopg2
from psycopg2 import sql


class HashMixin:
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        setattr(model_instance, self.attname, self.original)

    def get_placeholder(self, value=None, compiler=None, connection=None):
        return '%s'

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return sql.SQL("ENCRYPT(%s, %s)")
