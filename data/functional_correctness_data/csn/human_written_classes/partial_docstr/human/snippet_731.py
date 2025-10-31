from operator import methodcaller, index, attrgetter

class matchable:
    """Mixin for defining the operators on patterns.
    """

    def __or__(self, other):
        other = coerce_ellipsis(other)
        if self is other:
            return self
        if not isinstance(other, matchable):
            return NotImplemented
        patterns = []
        if isinstance(self, or_):
            patterns.extend(self.matchables)
        else:
            patterns.append(self)
        if isinstance(other, or_):
            patterns.extend(other.matchables)
        else:
            patterns.append(other)
        return or_(*patterns)

    def __ror__(self, other):
        if not isinstance(other, matchable):
            return NotImplemented
        return type(self).__or__(coerce_ellipsis(other), self)

    def __invert__(self):
        return not_(self)

    def __getitem__(self, key):
        try:
            n = index(key)
        except TypeError:
            pass
        else:
            return matchrange(self, n)
        if isinstance(key, tuple) and len(key) in (1, 2):
            return matchrange(self, *key)
        if isinstance(key, modifier):
            return postfix_modifier(self, key)
        raise TypeError('invalid modifier: {0}'.format(key))