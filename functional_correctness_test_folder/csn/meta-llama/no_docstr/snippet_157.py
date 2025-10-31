
import hashlib
import hmac


class HashMixin:

    def __init__(self, original=None, *args, **kwargs):
        if original is None:
            self.salt = kwargs.pop('salt', '')
            self.algorithm = kwargs.pop('algorithm', 'sha256')
        else:
            self.salt = original.salt
            self.algorithm = original.algorithm
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            setattr(model_instance, self.attname, self._hash_value(value))

    def get_placeholder(self, value=None, compiler=None, connection=None):
        return connection.ops.prep_for_like_query(self.get_encrypt_sql(connection)) + '(%s)'

    def get_encrypt_sql(self, connection):
        if self.algorithm == 'sha256':
            return 'SHA2'
        elif self.algorithm == 'md5':
            return 'MD5'
        else:
            raise ValueError('Unsupported algorithm')

    def _hash_value(self, value):
        if self.algorithm == 'sha256':
            return hmac.new(self.salt.encode(), value.encode(), hashlib.sha256).hexdigest()
        elif self.algorithm == 'md5':
            return hmac.new(self.salt.encode(), value.encode(), hashlib.md5).hexdigest()
        else:
            raise ValueError('Unsupported algorithm')
