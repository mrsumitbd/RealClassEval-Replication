class Module:

    def __init__(self, name, file=None, path=None):
        self.__name__ = name
        self.__file__ = file
        self.__path__ = path
        self.__code__ = None
        self.globalnames = {}
        self.starimports = {}

    def __repr__(self):
        s = 'Module(%r' % (self.__name__,)
        if self.__file__ is not None:
            s = s + ', %r' % (self.__file__,)
        if self.__path__ is not None:
            s = s + ', %r' % (self.__path__,)
        s = s + ')'
        return s