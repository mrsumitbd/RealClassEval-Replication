class TypedMixin:
    """Based class for enforcing types on lists and sets."""

    def __init__(self, iterable=[], types=[]):
        self._types = types
        if iterable:
            super().__init__(iterable)
            self._set_types()

    def _get_types(self):
        if not hasattr(self, '_types'):
            self._types = []
        if self._types == []:
            self._types = list(set([type(i) for i in self]))
        return self._types

    def _set_types(self):
        if self._types == []:
            self._types = list(set([type(i) for i in self]))
        else:
            raise Exception('Types have already been defined')
    types = property(fget=_get_types, fset=_set_types)

    def _check_type(self, value):
        if type(value) not in self.types and len(self.types) > 0:
            raise TypeError('This list cannot accept values of type ' + f'{type(value)}')