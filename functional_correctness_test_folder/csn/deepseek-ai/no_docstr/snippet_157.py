
class HashMixin:

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.original:
            setattr(model_instance, self.original,
                    getattr(model_instance, self.attname))

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if value is None:
            return '%s'
        return self.get_encrypt_sql(connection)

    def get_encrypt_sql(self, connection):
        raise NotImplementedError("Subclasses must implement get_encrypt_sql")
