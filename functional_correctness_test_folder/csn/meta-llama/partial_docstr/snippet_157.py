
from django.db.models import Field
from django.db.models.lookups import Exact, In, IsNull


class HashMixin(Field):
    '''Keyed hash mixin.
    `HashMixin` uses 'pgcrypto' to encrypt data in a postgres database.
    '''

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        '''Save the original_value.'''
        value = getattr(model_instance, self.attname)
        if self.original:
            setattr(model_instance, self.original, value)
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        return connection.ops.pg_encrypt_placeholder(self.get_encrypt_sql(connection), self)

    def get_encrypt_sql(self, connection):
        '''Get encrypt sql. This may be overidden by some implementations.'''
        return 'pgp_sym_encrypt(%s, %s)', [self.get_placeholder, connection.pgcrypto_key]

    def get_lookup(self, lookup_name):
        if lookup_name in ('exact', 'iexact'):
            return EncryptedExact
        elif lookup_name == 'in':
            return EncryptedIn
        elif lookup_name == 'isnull':
            return EncryptedIsNull
        return super().get_lookup(lookup_name)


class EncryptedExact(Exact):
    def process_rhs(self, qn, connection):
        rhs, params = super().process_rhs(qn, connection)
        params = [connection.pg_encrypt_value(
            p, self.lhs.output_field) for p in params]
        return rhs, params

    def as_sql(self, qn, connection):
        lhs_sql, lhs_params = self.process_lhs(qn, connection)
        rhs_sql, rhs_params = self.process_rhs(qn, connection)
        encrypt_sql, encrypt_params = self.lhs.output_field.get_encrypt_sql(
            connection)
        params = lhs_params + encrypt_params + rhs_params
        return f'{lhs_sql} = ' + encrypt_sql % rhs_sql, params


class EncryptedIn(In):
    def process_rhs(self, qn, connection):
        rhs, params = super().process_rhs(qn, connection)
        params = [connection.pg_encrypt_value(
            p, self.lhs.output_field) for p in params]
        return rhs, params

    def as_sql(self, qn, connection):
        lhs_sql, lhs_params = self.process_lhs(qn, connection)
        rhs_sql, rhs_params = self.process_rhs(qn, connection)
        encrypt_sql, encrypt_params = self.lhs.output_field.get_encrypt_sql(
            connection)
        params = lhs_params + encrypt_params + rhs_params
        return f'{lhs_sql} IN (' + ', '.join([encrypt_sql % rhs_sql] * len(rhs_params)) + ')', params


class EncryptedIsNull(IsNull):
    def as_sql(self, qn, connection):
        lhs_sql, lhs_params = self.process_lhs(qn, connection)
        encrypt_sql, encrypt_params = self.lhs.output_field.get_encrypt_sql(
            connection)
        if self.rhs:
            return f'{encrypt_sql % lhs_sql} IS NULL', lhs_params + encrypt_params
        else:
            return f'{encrypt_sql % lhs_sql} IS NOT NULL', lhs_params + encrypt_params
