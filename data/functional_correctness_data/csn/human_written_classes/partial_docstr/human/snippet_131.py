from time import monotonic

class time_limited:
    """
    Yield items from *iterable* until *limit_seconds* have passed.
    If the time limit expires before all items have been yielded, the
    ``timed_out`` parameter will be set to ``True``.

    >>> from time import sleep
    >>> def generator():
    ...     yield 1
    ...     yield 2
    ...     sleep(0.2)
    ...     yield 3
    >>> iterable = time_limited(0.1, generator())
    >>> list(iterable)
    [1, 2]
    >>> iterable.timed_out
    True

    Note that the time is checked before each item is yielded, and iteration
    stops if  the time elapsed is greater than *limit_seconds*. If your time
    limit is 1 second, but it takes 2 seconds to generate the first item from
    the iterable, the function will run for 2 seconds and not yield anything.
    As a special case, when *limit_seconds* is zero, the iterator never
    returns anything.

    """

    def __init__(self, limit_seconds, iterable):
        if limit_seconds < 0:
            raise ValueError('limit_seconds must be positive')
        self.limit_seconds = limit_seconds
        self._iterator = iter(iterable)
        self._start_time = monotonic()
        self.timed_out = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit_seconds == 0:
            self.timed_out = True
            raise StopIteration
        item = next(self._iterator)
        if monotonic() - self._start_time > self.limit_seconds:
            self.timed_out = True
            raise StopIteration
        return item