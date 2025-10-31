
class NiceRepr:
    def __nice__(self):
        if hasattr(self, '__len__'):
            return str(len(self))
        else:
            raise NotImplementedError(
                f'Define the __nice__ method for {self.__class__.__name__!r}')

    def __repr__(self):
        try:
            nice = self.__nice__()
        except Exception as ex:
            import warnings
            warnings.warn(
                f'Error in {self.__class__.__name__}.__nice__: {ex}', RuntimeWarning)
            nice = ''
        classname = self.__class__.__name__
        return f'<{classname}({nice}) at {hex(id(self))}>'

    def __str__(self):
        try:
            nice = self.__nice__()
        except Exception as ex:
            import warnings
            warnings.warn(
                f'Error in {self.__class__.__name__}.__nice__: {ex}', RuntimeWarning)
            nice = ''
        classname = self.__class__.__name__
        return f'<{classname}({nice})>'
