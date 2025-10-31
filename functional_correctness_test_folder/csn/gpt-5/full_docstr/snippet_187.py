class NodeFinder:
    '''
    Find nodes based on flexable criteria.  The I{matcher} is
    may be any object that implements a match(n) method.
    @ivar matcher: An object used as criteria for match.
    @type matcher: I{any}.match(n)
    @ivar limit: Limit the number of matches.  0=unlimited.
    @type limit: int
    '''

    def __init__(self, matcher, limit=0):
        '''
        @param matcher: An object used as criteria for match.
        @type matcher: I{any}.match(n)
        @param limit: Limit the number of matches.  0=unlimited.
        @type limit: int
        '''
        self.matcher = matcher
        self.limit = int(limit) if limit is not None else 0

    def _match(self, node):
        m = getattr(self.matcher, "match", None)
        if callable(m):
            return bool(m(node))
        if callable(self.matcher):
            return bool(self.matcher(node))
        return False

    def _children_of(self, node):
        # Try common child containers
        for attr in ("children", "childNodes", "contents", "nodes"):
            if hasattr(node, attr):
                children = getattr(node, attr)
                if children is not None:
                    try:
                        return list(children)
                    except TypeError:
                        pass
        # Methods possibly returning children
        for meth in ("getChildren", "iterchildren", "iterChildren", "get_children"):
            f = getattr(node, meth, None)
            if callable(f):
                children = f()
                try:
                    return list(children)
                except TypeError:
                    pass
        # If node itself is iterable (but not a string/bytes), treat as container
        if hasattr(node, "__iter__") and not isinstance(node, (str, bytes, bytearray)):
            try:
                return list(iter(node))
            except TypeError:
                pass
        return []

    def _recurse(self, node, out_list):
        if node is None:
            return False
        if self._match(node):
            out_list.append(node)
            if self.limit and len(out_list) >= self.limit:
                return True  # reached limit
        for child in self._children_of(node):
            if self._recurse(child, out_list):
                return True
        return False

    def find(self, node, list):
        '''
        Traverse the tree looking for matches.
        @param node: A node to match on.
        @type node: L{SchemaObject}
        @param list: A list to fill.
        @type list: list
        '''
        if list is None:
            raise ValueError("list must be a list to fill")
        self._recurse(node, list)
        return list
