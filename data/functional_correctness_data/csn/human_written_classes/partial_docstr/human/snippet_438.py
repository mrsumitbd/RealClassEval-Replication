import functools

class memoize_method:
    """
    memoization decorator for a method that respects args and kwargs

    References:
        .. [ActiveState_Miller_2010] http://code.activestate.com/recipes/577452-a-memoize-decorator-for-instance-methods

    Attributes:
        __func__ (Callable): the wrapped function

    Note:
        This is very thread-unsafe, and has an issue as pointed out in
        [ActiveState_Miller_2010]_, next version may work on fixing this.

    Example:
        >>> import ubelt as ub
        >>> closure1 = closure = {'a': 'b', 'c': 'd', 'z': 'z1'}
        >>> incr = [0]
        >>> class Foo:
        >>>     def __init__(self, instance_id):
        >>>         self.instance_id = instance_id
        >>>     @ub.memoize_method
        >>>     def foo_memo(self, key):
        >>>         "Wrapped foo_memo docstr"
        >>>         value = closure[key]
        >>>         incr[0] += 1
        >>>         return value, self.instance_id
        >>>     def foo(self, key):
        >>>         value = closure[key]
        >>>         incr[0] += 1
        >>>         return value, self.instance_id
        >>> self1 = Foo('F1')
        >>> assert self1.foo('a') == ('b', 'F1')
        >>> assert self1.foo('c') == ('d', 'F1')
        >>> assert incr[0] == 2
        >>> #
        >>> print('Call memoized version')
        >>> assert self1.foo_memo('a') == ('b', 'F1')
        >>> assert self1.foo_memo('c') == ('d', 'F1')
        >>> assert incr[0] == 4, 'should have called a function 4 times'
        >>> #
        >>> assert self1.foo_memo('a') == ('b', 'F1')
        >>> assert self1.foo_memo('c') == ('d', 'F1')
        >>> print('Counter should no longer increase')
        >>> assert incr[0] == 4
        >>> #
        >>> print('Closure changes result without memoization')
        >>> closure2 = closure = {'a': 0, 'c': 1, 'z': 'z2'}
        >>> assert self1.foo('a') == (0, 'F1')
        >>> assert self1.foo('c') == (1, 'F1')
        >>> assert incr[0] == 6
        >>> assert self1.foo_memo('a') == ('b', 'F1')
        >>> assert self1.foo_memo('c') == ('d', 'F1')
        >>> #
        >>> print('Constructing a new object should get a new cache')
        >>> self2 = Foo('F2')
        >>> self2.foo_memo('a')
        >>> assert incr[0] == 7
        >>> self2.foo_memo('a')
        >>> assert incr[0] == 7
        >>> # Check that the decorator preserves the name and docstring
        >>> assert self1.foo_memo.__doc__ == 'Wrapped foo_memo docstr'
        >>> assert self1.foo_memo.__name__ == 'foo_memo'
        >>> print(f'self1.foo_memo = {self1.foo_memo!r}, {hex(id(self1.foo_memo))}')
        >>> print(f'self2.foo_memo = {self2.foo_memo!r}, {hex(id(self2.foo_memo))}')
        >>> #
        >>> # Test for the issue in the active state recipe
        >>> method1 = self1.foo_memo
        >>> method2 = self2.foo_memo
        >>> assert method1('a') == ('b', 'F1')
        >>> assert method2('a') == (0, 'F2')
        >>> assert method1('z') == ('z2', 'F1')
        >>> assert method2('z') == ('z2', 'F2')
    """

    def __init__(self, func):
        """
        Args:
            func (Callable): method to wrap
        """
        self._func = func
        self._cache_name = '_cache__' + func.__name__
        self.__func__ = func
        functools.update_wrapper(self, func)

    def __get__(self, instance, cls=None):
        """
        Descriptor get method. Called when the decorated method is accessed
        from an object instance.

        Args:
            instance (object): the instance of the class with the memoized method
            cls (type | None): the type of the instance
        """
        import types
        unbound = self._func
        cache = instance.__dict__.setdefault(self._cache_name, {})

        @functools.wraps(unbound)
        def memoizer(instance, *args, **kwargs):
            key = _make_signature_key(args, kwargs)
            if key not in cache:
                cache[key] = unbound(instance, *args, **kwargs)
            return cache[key]
        bound_memoizer = types.MethodType(memoizer, instance)
        setattr(instance, self._func.__name__, bound_memoizer)
        return bound_memoizer