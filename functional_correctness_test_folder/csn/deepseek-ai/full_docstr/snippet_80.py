
class NiceRepr:
    def __nice__(self):
        if hasattr(self, '__len__'):
            return str(len(self))
        else:
            raise RuntimeWarning(
                f'No __nice__ method defined for {self.__class__.__name__}. '
                'Define __nice__ or __len__ for a default implementation.'
            )

    def __repr__(self):
        try:
            nice = self.__nice__()
        except Exception as ex:
            if isinstance(ex, RuntimeWarning):
                import warnings
                warnings.warn(str(ex), RuntimeWarning)
            nice = '...'
        classname = self.__class__.__name__
        return f'<{classname}({nice}) at {hex(id(self))}>'

    def __str__(self):
        try:
            nice = self.__nice__()
        except Exception as ex:
            if isinstance(ex, RuntimeWarning):
                import warnings
                warnings.warn(str(ex), RuntimeWarning)
            nice = '...'
        classname = self.__class__.__name__
        return f'<{classname}({nice})>'
