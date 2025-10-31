
import functools


class EventInterceptor:
    """
    Context‑manager that temporarily replaces methods on a source object
    with wrappers that invoke user‑supplied callbacks before delegating
    to the original method.

    Example
    -------
    >>> class Foo:
    ...     def bar(self, x):
    ...         return x * 2
    ...
    >>> def on_bar(self, x):
    ...     print(f"bar called with {x}")
    ...
    >>> foo = Foo()
    >>> with EventInterceptor(foo, bar=on_bar):
    ...     foo.bar(5)          # prints "bar called with 5" and returns 10
    """

    def __init__(self, source, **events):
        """
        Parameters
        ----------
        source : object
            The object whose methods will be intercepted.
        **events : callable
            Mapping of method names to callback functions. Each callback
            will be called with the same arguments as the original method.
        """
        self._source = source
        self._events = events
        self._originals = {}

    def __enter__(self):
        for name, callback in self._events.items():
            if not hasattr(self._source, name):
                continue
            original = getattr(self._source, name)
            if not callable(original):
                continue
            self._originals[name] = original

            @functools.wraps(original)
            def wrapper(*args, _orig=original, _cb=callback, **kwargs):
                _cb(*args, **kwargs)
                return _orig(*args, **kwargs)

            setattr(self._source, name, wrapper)
        return self

    def __exit__(self, typ, value, traceback):
        for name, original in self._originals.items():
            setattr(self._source, name, original)
        self._originals.clear()
        # Do not suppress exceptions
        return False
