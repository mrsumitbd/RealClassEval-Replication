
class HashMixin:

    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            setattr(model_instance, self.attname, self.encrypt(value))
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if value is not None:
            return '%s'
        return '%s'

    def get_encrypt_sql(self, connection):
        return f"ENCRYPT({self.get_placeholder()})"

    def encrypt(self, value):
        # Example encryption logic (not secure for real use)
        import hashlib
        return hashlib.sha256(value.encode()).hexdigest()
