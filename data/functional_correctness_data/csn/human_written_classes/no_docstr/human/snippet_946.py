import functools

class _WithParameterMixin:

    @functools.cached_property
    def parameter(self):
        return self.related('parameterReference')

    @property
    def parameters(self):
        return self.all_related('parameterReference')