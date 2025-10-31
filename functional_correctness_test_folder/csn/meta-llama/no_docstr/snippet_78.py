
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

    def __getitem__(self, key):
        try:
            import js  # pyodide
            data = js.sessionStorage.getItem(key)
            if data is None:
                raise KeyError(key)
            return json.loads(data)
        except ImportError:
            raise NotImplementedError(
                "Cache is only available in a pyodide environment")

    def __setitem__(self, key, value):
        try:
            import js  # pyodide
            js.sessionStorage.setItem(key, json.dumps(value))
        except ImportError:
            raise NotImplementedError(
                "Cache is only available in a pyodide environment")
