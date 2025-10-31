class TnsFilter:

    def __init__(self, *tns):
        self._tns = set()
        if tns:
            self.add(*tns)

    def add(self, *tns):
        def _iter(items):
            for it in items:
                if it is None:
                    continue
                if isinstance(it, (list, tuple, set, frozenset)):
                    for sub in it:
                        yield sub
                else:
                    yield it

        for ns in _iter(tns):
            if isinstance(ns, str) and ns.strip():
                self._tns.add(ns)

    def match(self, root, ns):
        '''
        Match by I{targetNamespace} excluding those that
        are equal to the specified namespace to prevent
        adding an import to itself.
        @param root: A schema root.
        @type root: L{Element}
        '''
        if root is None:
            return False
        get_attr = getattr(root, "get", None)
        if not callable(get_attr):
            return False
        target_ns = root.get("targetNamespace")
        if not target_ns:
            return False
        if target_ns == ns:
            return False
        if not self._tns:
            return True
        return target_ns in self._tns
