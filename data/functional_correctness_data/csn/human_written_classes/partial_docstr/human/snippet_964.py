class FixedValues:
    """Utility class to store fixed values"""

    def __init__(self, **kwds):
        self._params = kwds

    def __getattr__(self, name):
        return self._params[name]