import attr

@attr.s
class CompareResult:
    """Hold comparison results in logical tree."""
    result = attr.ib(default=None)
    type = attr.ib(default=None)
    ref = attr.ib(default=None)
    changes = attr.ib(default=None)
    _children = attr.ib(factory=list)

    def add_child(self, child):
        self._children.append(child)

    @property
    def children(self):
        return self._children