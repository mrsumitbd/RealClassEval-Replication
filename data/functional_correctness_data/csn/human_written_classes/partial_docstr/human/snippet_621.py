import weakref

class MockMap:

    def __init__(self, original):
        """ Wrap a mock mapping around the original one-to-many relation. """
        self.map = {}
        self.original = original

    def __set__(self, instance, value):
        """ Set a related object for an instance. """
        self.map[id(instance)] = (weakref.ref(instance), value)

    def __getattr__(self, name):
        """ Delegate all other calls to the original. """
        return getattr(self.original, name)