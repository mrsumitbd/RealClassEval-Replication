class GroupResolver:

    def __init__(self, include=None, exclude=None, all_groups=False, default=True):
        self._include = frozenset(include or ())
        self._exclude = frozenset(exclude or ())
        self._all = all_groups
        self._default = default

    def match(self, groups):
        if not groups:
            return self._default
        groups = {str(e) for e in groups}
        exclude = groups.intersection(self._exclude)
        include = groups.intersection(self._include)
        if self._all:
            if exclude:
                return ()
        elif not include:
            return ()
        return groups