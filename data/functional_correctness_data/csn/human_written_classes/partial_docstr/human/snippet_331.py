class DictWrapper:
    """provide attribute-style access to a nested dict"""

    def __init__(self, d, prefix=''):
        object.__setattr__(self, 'd', d)
        object.__setattr__(self, 'prefix', prefix)

    def __setattr__(self, key, val):
        prefix = object.__getattribute__(self, 'prefix')
        if prefix:
            prefix += '.'
        prefix += key
        if key in self.d and (not isinstance(self.d[key], dict)):
            _set_option(prefix, val)
        else:
            raise OptionError('You can only set the value of existing options')

    def __getattr__(self, key):
        prefix = object.__getattribute__(self, 'prefix')
        if prefix:
            prefix += '.'
        prefix += key
        v = object.__getattribute__(self, 'd')[key]
        if isinstance(v, dict):
            return DictWrapper(v, prefix)
        else:
            return _get_option(prefix)

    def __dir__(self):
        return list(self.d.keys())