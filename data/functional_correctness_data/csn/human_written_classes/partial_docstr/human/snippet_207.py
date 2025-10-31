import pickle

class PickleSerializer:
    """Simple wrapper around Pickle for signing.dumps and signing.loads."""

    @staticmethod
    def dumps(obj) -> bytes:
        return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def loads(data) -> any:
        return pickle.loads(data)