class Struct:
    __slots__ = ()
    _all_field_names_ = set()

    def __eq__(self, other):
        if not isinstance(other, Struct):
            return False
        if self._all_field_names_ != other._all_field_names_:
            return False
        if not isinstance(other, self.__class__) and (not isinstance(self, other.__class__)):
            return False
        for field_name in self._all_field_names_:
            if getattr(self, field_name) != getattr(other, field_name):
                return False
        return True

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        args = ['{}={!r}'.format(name, getattr(self, '_{}_value'.format(name))) for name in sorted(self._all_field_names_)]
        return '{}({})'.format(type(self).__name__, ', '.join(args))

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        pass