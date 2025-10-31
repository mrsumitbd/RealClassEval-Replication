
import hashlib


class HashMixin:

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value is not None and (self.original is None or value != self.original):
            hashed = hashlib.sha256(str(value).encode('utf-8')).hexdigest()
            setattr(model_instance, self.attname, hashed)
            self.original = hashed
            return hashed
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        return '%s'

    def get_encrypt_sql(self, connection):
        return "SHA2(%s, 256)"
