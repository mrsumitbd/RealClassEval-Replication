
class NiceRepr:
    def __nice__(self):
        if hasattr(self, '__len__'):
            return str(len(self))
        else:
            import warnings
            warnings.warn('object at {0} has no __nice__ method'.format(
                hex(id(self))), RuntimeWarning)
            return 'object at {0}'.format(hex(id(self)))

    def __repr__(self):
        try:
            nice = self.__nice__()
        except Exception:
            import warnings
            warnings.warn('object at {0} has a buggy __nice__ method'.format(
                hex(id(self))), RuntimeWarning)
            nice = 'object at {0}'.format(hex(id(self)))
        classname = self.__class__.__name__
        return '<{0}({1}) at {2}>'.format(classname, nice, hex(id(self)))

    def __str__(self):
        try:
            nice = self.__nice__()
        except Exception:
            import warnings
            warnings.warn('object at {0} has a buggy __nice__ method'.format(
                hex(id(self))), RuntimeWarning)
            nice = 'object at {0}'.format(hex(id(self)))
        classname = self.__class__.__name__
        return '<{0}({1})>'.format(classname, nice)
