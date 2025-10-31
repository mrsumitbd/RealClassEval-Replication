from threading import Lock

class cached_property:
    """ thread safe cached property """

    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__
        self.lock = Lock()

    def __get__(self, instance, cls=None):
        with self.lock:
            if instance is None:
                return self
            try:
                return instance.__dict__[self.name]
            except KeyError:
                res = instance.__dict__[self.name] = self.func(instance)
                return res