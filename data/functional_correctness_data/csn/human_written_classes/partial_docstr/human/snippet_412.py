class LegacyWrappingSerde:
    """
    This class defines how to wrap legacy de/serialization functions into a
    'serde' object which implements '.serialize' and '.deserialize' methods.
    It is used automatically by pymemcache.client.base.Client when the
    'serializer' or 'deserializer' arguments are given.

    The serializer_func and deserializer_func are expected to be None in the
    case that they are missing.
    """

    def __init__(self, serializer_func, deserializer_func) -> None:
        self.serialize = serializer_func or self._default_serialize
        self.deserialize = deserializer_func or self._default_deserialize

    def _default_serialize(self, key, value):
        return (value, 0)

    def _default_deserialize(self, key, value, flags):
        return value