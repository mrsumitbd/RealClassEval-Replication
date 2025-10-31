
import json
import numpy as np


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
        value = self._get_session_storage(key)
        if value is not None:
            return json.loads(value)
        raise KeyError(key)

    def __setitem__(self, key, value):
        if isinstance(value, np.ndarray):
            value = value.tolist()
        self._set_session_storage(key, json.dumps(value))

    def _get_session_storage(self, key):
        from js import sessionStorage
        return sessionStorage.getItem(key)

    def _set_session_storage(self, key, value):
        from js import sessionStorage
        sessionStorage.setItem(key, value)
