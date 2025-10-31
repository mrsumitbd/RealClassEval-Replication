
import warnings


class NiceRepr:
    def __nice__(self):
        if hasattr(self, '__len__'):
            return str(len(self))
        else:
            warnings.warn(
                f'No __nice__ method defined for {self.__class__.__name__}, defaulting to object at {hex(id(self))}', RuntimeWarning)
            return f'object at {hex(id(self))}'

    def __repr__(self):
        try:
            nice = self.__nice__()
        except Exception:
            warnings.warn(
                f'Error in __nice__ method for {self.__class__.__name__}, defaulting to object at {hex(id(self))}', RuntimeWarning)
            nice = f'object at {hex(id(self))}'
        classname = self.__class__.__name__
        return f'<{classname}({nice}) at {hex(id(self))}>'

    def __str__(self):
        try:
            nice = self.__nice__()
        except Exception:
            warnings.warn(
                f'Error in __nice__ method for {self.__class__.__name__}, defaulting to object at {hex(id(self))}', RuntimeWarning)
            nice = f'object at {hex(id(self))}'
        classname = self.__class__.__name__
        return f'<{classname}({nice})>'
