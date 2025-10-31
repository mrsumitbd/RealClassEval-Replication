class _BunserDict:
    __slots__ = ('_keys', '_values')

    def __init__(self, keys, values):
        self._keys = keys
        self._values = values

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __getitem__(self, key):
        if isinstance(key, (int, long)):
            return self._values[key]
        elif key.startswith('st_'):
            key = key[3:]
        try:
            return self._values[self._keys.index(key)]
        except ValueError:
            raise KeyError('_BunserDict has no key %s' % key)

    def __len__(self):
        return len(self._keys)