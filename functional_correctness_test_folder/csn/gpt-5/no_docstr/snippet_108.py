class Details:
    def __init__(self, details):
        from collections.abc import Mapping

        def wrap(value):
            if isinstance(value, Mapping):
                return Details(value)
            if isinstance(value, list):
                return [wrap(v) for v in value]
            if isinstance(value, tuple):
                return tuple(wrap(v) for v in value)
            if isinstance(value, set):
                return {wrap(v) for v in value}
            return value

        if details is None:
            details = {}
        elif isinstance(details, Details):
            details = details.all
        elif not isinstance(details, Mapping):
            raise TypeError("details must be a mapping or Details instance")

        wrapped = {k: wrap(v) for k, v in details.items()}
        object.__setattr__(self, "_details", wrapped)

    def __getattr__(self, attr):
        d = object.__getattribute__(self, "_details")
        try:
            return d[attr]
        except KeyError:
            raise AttributeError(
                f"{type(self).__name__!s} has no attribute '{attr}'")

    @property
    def all(self):
        def unwrap(value):
            if isinstance(value, Details):
                return value.all
            if isinstance(value, list):
                return [unwrap(v) for v in value]
            if isinstance(value, tuple):
                return tuple(unwrap(v) for v in value)
            if isinstance(value, set):
                return {unwrap(v) for v in value}
            return value

        return {k: unwrap(v) for k, v in self._details.items()}
