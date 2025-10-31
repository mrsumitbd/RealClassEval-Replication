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
    _storage = {}

    def __getitem__(self, key):
        '''Load the value stored with the key.
        Parameters
        ----------
        key : str
            The key to lookup the value stored.
        Returns
        -------
        object
            The value if the key exists in the cache, otherwise None.
        '''
        import json
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        raw = self._storage.get(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def __setitem__(self, key, value):
        import json

        if not isinstance(key, str):
            raise TypeError("key must be a string")

        def _default(obj):
            try:
                import numpy as np  # noqa
                import numpy
                if isinstance(obj, numpy.generic):
                    return obj.item()
                if hasattr(obj, "tolist"):
                    return obj.tolist()
            except Exception:
                pass
            if isinstance(obj, (set, frozenset)):
                return list(obj)
            if isinstance(obj, bytes):
                return obj.decode("utf-8", errors="replace")
            raise TypeError(
                f"Object of type {type(obj).__name__} is not JSON serializable")

        serialized = json.dumps(value, default=_default)
        self._storage[key] = serialized
