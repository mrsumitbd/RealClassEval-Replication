class FakeCache:
    """
    An object that mimics just enough of Flask-Caching's API to be compatible
    with our needs, but does nothing.
    """

    def get(self, key):
        return None

    def set(self, key, value):
        return None

    def delete(self, key):
        return None