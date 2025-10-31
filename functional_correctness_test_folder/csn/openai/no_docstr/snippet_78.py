
import json

try:
    # In a browser environment (e.g., Pyodide) the `js` module provides access to
    # the browser's JavaScript APIs, including sessionStorage.
    import js
    _HAS_JS = True
except Exception:
    _HAS_JS = False


class _Cache:
    """Store data in the browser.

    This cache uses session storage so data will stay in the browser until the
    tab is closed. All data must be serializable, which means if the
    serialization transforms the data it won't be the same when it is fetched.

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
        # Fallback storage for non-browser environments
        self._fallback = {}

    def __getitem__(self, key):
        key = str(key)
        if _HAS_JS:
            raw = js.sessionStorage.getItem(key)
            if raw is None:
                raise KeyError(key)
            return json.loads(raw)
        else:
            if key not in self._fallback:
                raise KeyError(key)
            return self._fallback[key]

    def __setitem__(self, key, value):
        key = str(key)
        # Convert NumPy arrays (or any object with tolist) to plain lists
        if hasattr(value, "tolist"):
            value = value.tolist()
        serialized = json.dumps(value)
        if _HAS_JS:
            js.sessionStorage.setItem(key, serialized)
        else:
            self._fallback[key] = value
