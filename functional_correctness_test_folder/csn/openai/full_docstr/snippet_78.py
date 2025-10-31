
import json

try:
    # In a browser environment (e.g. Pyodide) we can access the JavaScript sessionStorage
    from js import sessionStorage as _js_session_storage
except Exception:
    _js_session_storage = None

try:
    import numpy as _np
except Exception:
    _np = None


class _Cache:
    """Store data in the browser.

    This cache uses session storage so data will stay in the browser until the tab is closed.
    All data must be serializable, which means if the serialization transforms the data it won't be the same
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
    """

    def __init__(self):
        # Use the browser's sessionStorage if available, otherwise fall back to a dict
        self._storage = _js_session_storage if _js_session_storage is not None else {}

    def __getitem__(self, key):
        """Load the value stored with the key.

        Parameters
        ----------
        key : str
            The key to lookup the value stored.

        Returns
        -------
        object
            The value if the key exists in the cache, otherwise None.
        """
        key = str(key)
        try:
            if hasattr(self._storage, "getItem"):
                raw = self._storage.getItem(key)
            else:
                raw = self._storage.get(key)
        except Exception:
            return None

        if raw is None:
            return None

        try:
            return json.loads(raw)
        except Exception:
            return None

    def __setitem__(self, key, value):
        """Store the key value pair.

        Parameters
        ----------
        key : str
            The key to determine where it's stored, you'll need this to load the value later.
        value : object
            The value to store in the cache.

        Returns
        -------
        None
        """
        key = str(key)

        def _default(o):
            if _np is not None and isinstance(o, _np.ndarray):
                return o.tolist()
            raise TypeError(
                f"Object of type {type(o).__name__} is not JSON serializable")

        try:
            raw = json.dumps(value, default=_default)
        except Exception:
            # Fallback: store the string representation
            raw = str(value)

        try:
            if hasattr(self._storage, "setItem"):
                self._storage.setItem(key, raw)
            else:
                self._storage[key] = raw
        except Exception:
            pass
