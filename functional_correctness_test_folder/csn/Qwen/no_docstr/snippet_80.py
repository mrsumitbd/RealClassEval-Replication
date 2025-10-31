
class NiceRepr:
    def __nice__(self):
        try:
            return str(len(self))
        except (TypeError, NotImplementedError):
            return ''

    def __repr__(self):
        nice = self.__nice__()
        classname = self.__class__.__name__
        return f'<{classname}({nice}) at {hex(id(self))}>'

    def __str__(self):
        nice = self.__nice__()
        classname = self.__class__.__name__
        return f'<{classname}({nice})>'
