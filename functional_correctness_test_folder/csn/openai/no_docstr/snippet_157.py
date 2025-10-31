
import hashlib


class HashMixin:
    """
    A mixin that hashes a field's value before saving.
    """

    def __init__(self, original=None, *args, **kwargs):
        """
        Initialize the mixin with an optional original value.
        """
        super().__init__(*args, **kwargs)
        self.original = original

    def _hash_value(self, value):
        """
        Return a SHA‑256 hex digest of the given value.
        """
        if value is None:
            return None
        if isinstance(value, bytes):
            data = value
        else:
            data = str(value).encode("utf-8")
        return hashlib.sha256(data).hexdigest()

    def pre_save(self, model_instance, add):
        """
        Hash the field value before saving if it has changed.
        """
        # Retrieve the current value from the model instance
        value = getattr(model_instance, self.attname, None)

        # If this is a new instance or the value has changed, hash it
        if add or value != self.original:
            hashed = self._hash_value(value)
            # Store the hashed value back on the instance
            setattr(model_instance, self.attname, hashed)
            # Update the original to the new value (unhashed)
            self.original = value
            return hashed

        # No change – return the existing value
        return value

    def get_placeholder(self, value=None, compiler=None, connection=None):
        """
        Return the placeholder used in SQL statements.
        """
        # Django uses '%s' as the placeholder for most backends
        return "%s"

    def get_encrypt_sql(self, connection):
        """
        Return an SQL expression that hashes the value.
        """
        # Use the database's SHA2 function if available; otherwise fall back to
        # a generic placeholder that can be replaced by the backend.
        # This is a simple example and may need adjustment for specific DBs.
        return "SHA2(%s, 256)"
