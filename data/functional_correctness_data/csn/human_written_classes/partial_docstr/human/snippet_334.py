class DeprecationHelper:
    """Deprecation helper for classes and functions.

    Based on https://stackoverflow.com/a/9008509/8727928
    """

    def __init__(self, new_target, msg=None):
        self.new_target = new_target
        self.msg = msg

    def _warn(self):
        from warnings import warn
        if self.msg is None:
            msg = 'This class will get deprecated.'
        else:
            msg = self.msg
        warn(msg, DeprecationWarning, stacklevel=1)

    def __call__(self, *args, **kwargs):
        self._warn()
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        self._warn()
        return getattr(self.new_target, attr)