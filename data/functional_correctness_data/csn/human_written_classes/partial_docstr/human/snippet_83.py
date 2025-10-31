import inspect
import functools
import copy
import weakref

class cache_randomness:
    """Decorator that marks the method with random return value(s) in a
    transform class.

    This decorator is usually used together with the context-manager
    :func`:cache_random_params`. In this context, a decorated method will
    cache its return value(s) at the first time of being invoked, and always
    return the cached values when being invoked again.

    .. note::
        Only an instance method can be decorated with ``cache_randomness``.
    """

    def __init__(self, func):
        if not inspect.isfunction(func):
            raise TypeError('Unsupport callable to decorate with@cache_randomness.')
        func_args = inspect.getfullargspec(func).args
        if len(func_args) == 0 or func_args[0] != 'self':
            raise TypeError('@cache_randomness should only be used to decorate instance methods (the first argument is ``self``).')
        functools.update_wrapper(self, func)
        self.func = func
        self.instance_ref = None

    def __set_name__(self, owner, name):
        if not hasattr(owner, '_methods_with_randomness'):
            setattr(owner, '_methods_with_randomness', [])
        owner._methods_with_randomness.append(name)

    def __call__(self, *args, **kwargs):
        instance = self.instance_ref()
        name = self.__name__
        cache_enabled = getattr(instance, '_cache_enabled', False)
        if cache_enabled:
            if not hasattr(instance, '_cache'):
                setattr(instance, '_cache', {})
            if name not in instance._cache:
                instance._cache[name] = self.func(instance, *args, **kwargs)
            return instance._cache[name]
        else:
            if hasattr(instance, '_cache'):
                del instance._cache
            return self.func(instance, *args, **kwargs)

    def __get__(self, obj, cls):
        self.instance_ref = weakref.ref(obj)
        return copy.copy(self)