class _ClientConfigDescriptor:

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        return obj.__dict__[self.name]

    def __set__(self, obj, value) -> None:
        obj.__dict__[self.name] = value