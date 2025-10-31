
class HashMixin:

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if self.original is not None:
            value = self.value_from_object(model_instance)
            if value != self.original:
                self.original = value
                return True
        return False

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if value is None:
            value = self.value
        if compiler is None:
            connection = connection or self.connection
            compiler = connection.ops.compiler(connection)
        return compiler.compile(self.get_encrypt_sql(connection))

    def get_encrypt_sql(self, connection):
        return connection.ops.encrypt_sql(self)
