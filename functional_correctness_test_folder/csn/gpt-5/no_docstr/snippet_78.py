import json


class _Cache:
    '''Store data in the browser.
    This cache uses session storage so data will stay
    in the browser until the tab is closed.
    All data must be serializable, which means if the
    serialization transforms the data it won't be the same
    when it is fetched.
    Examples
    --------
    >>> from bowtie import cache
    >>> cache['a'] = True  # doctest: +SKIP
    >>> cache['a']  # doctest: +SKIP
    True
    >>> cache['b'] = np.arange(5)  # doctest: +SKIP
    >>> cache['b']  # doctest: +SKIP
    [1, 2, 3, 4, 5]
    '''
    _store = {}

    def __getitem__(self, key):
        k = str(key)
        if k not in self._store:
            raise KeyError(key)
        return json.loads(self._store[k])

    def __setitem__(self, key, value):
        def _default(o):
            if hasattr(o, "tolist"):
                return o.tolist()
            if isinstance(o, (set, tuple)):
                return list(o)
            if isinstance(o, bytes):
                return o.decode("utf-8")
            raise TypeError(
                f"Object of type {type(o).__name__} is not JSON serializable")

        self._store[str(key)] = json.dumps(value, default=_default)
