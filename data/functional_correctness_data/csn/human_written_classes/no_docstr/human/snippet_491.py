class Route:
    __slots__ = ('name', 'version', 'deprecated', 'arg_type', 'result_type', 'error_type', 'attrs')

    def __init__(self, name, version, deprecated, arg_type, result_type, error_type, attrs):
        self.name = name
        self.version = version
        self.deprecated = deprecated
        self.arg_type = arg_type
        self.result_type = result_type
        self.error_type = error_type
        assert isinstance(attrs, dict), 'Expected dict, got %r' % attrs
        self.attrs = attrs

    def __repr__(self):
        return 'Route({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(self.name, self.version, self.deprecated, self.arg_type, self.result_type, self.error_type, self.attrs)