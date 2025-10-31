
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
        from js import sessionStorage
        value = sessionStorage.getItem(key)
        if value is not None:
            return json.loads(value)
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
        from js import sessionStorage
        sessionStorage.setItem(key, json.dumps(value))
