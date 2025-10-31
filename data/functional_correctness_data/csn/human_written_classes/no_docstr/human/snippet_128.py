class SynchroGridOutProperty:

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype):
        obj.synchronize(obj.delegate.open)()
        return getattr(obj.delegate, self.name)