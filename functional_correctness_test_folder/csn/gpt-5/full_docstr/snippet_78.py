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
        data = self._storage.get(key)
        if data is None:
            return None

        def object_hook(obj):
            if isinstance(obj, dict) and obj.get('__type__') == 'bytes':
                import base64
                return base64.b64decode(obj['data'])
            return obj

        try:
            return json.loads(data, object_hook=object_hook)
        except Exception:
            return None

    def __setitem__(self, key, value):
        '''Store the key value pair.
        Parameters
        ----------
        key : str
            The key to determine where it's stored, you'll need this to load the value later.
        value : object
            The value to store in the cache.
        Returns
        -------
        None
        '''
        import json

        def default(o):
            # Numpy support (optional)
            try:
                import numpy as np  # noqa: F401
                import numpy as _np
                if isinstance(o, _np.ndarray):
                    return o.tolist()
                if isinstance(o, (_np.integer,)):
                    return int(o)
                if isinstance(o, (_np.floating,)):
                    return float(o)
                if isinstance(o, (_np.bool_,)):
                    return bool(o)
            except Exception:
                pass

            # Bytes as base64
            if isinstance(o, (bytes, bytearray, memoryview)):
                import base64
                return {
                    '__type__': 'bytes',
                    'data': base64.b64encode(bytes(o)).decode('ascii'),
                }

            # Sets/tuples become lists (may not round-trip type)
            if isinstance(o, (set, tuple)):
                return list(o)

            # Fallback: try to use string representation
            try:
                return str(o)
            except Exception:
                raise TypeError(
                    f'Object of type {type(o).__name__} is not JSON serializable')

        payload = json.dumps(value, default=default, ensure_ascii=False)
        self._storage[key] = payload
