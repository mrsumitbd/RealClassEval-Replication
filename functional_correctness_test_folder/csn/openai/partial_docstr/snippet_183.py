class Reader:
    '''
    The reader provides integration with cache.
    @ivar options: An options object.
    @type options: I{Options}
    '''

    def __init__(self, options):
        self.options = options

    def mangle(self, name, x):
        """
        Generate a cache key by combining the given name and value `x`.
        If the options object defines a `prefix` attribute, it will be
        prepended to the key.  The separator used between components is
        taken from the options' `separator` attribute if present,
        otherwise a colon ':' is used.
        """
        prefix = getattr(self.options, 'prefix', None)
        separator = getattr(self.options, 'separator', ':')
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(name)
        parts.append(str(x))
        return separator.join(parts)
