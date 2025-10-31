
import json
try:
    # Pyodide / JupyterLite environment
    from js import sessionStorage
except Exception:
    # Fallback: no browser storage available
    sessionStorage = None


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
        if sessionStorage is None:
            return None
        raw = sessionStorage.getItem(key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def __setitem__(self, key, value):
        if sessionStorage is None:
            return
        # Serialize value to JSON, handling numpy arrays and other non-JSON types

        def default(o):
            try:
                return o.tolist()
            except Exception:
                return str(o)
        try:
            raw = json.dumps(value, default=default)
            sessionStorage.setItem(key, raw)
        except Exception:
            # If serialization fails, do nothing
            pass
