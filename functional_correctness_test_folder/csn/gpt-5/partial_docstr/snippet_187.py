class NodeFinder:
    '''
    Find nodes based on flexable criteria.  The matcher
    may be any object that implements a match(n) method.
    @ivar matcher: An object used as criteria for match.
    @type matcher: any with .match(n)
    @ivar limit: Limit the number of matches.  0=unlimited.
    @type limit: int
    '''

    def __init__(self, matcher, limit=0):
        '''
        @param matcher: An object used as criteria for match.
        @type matcher: any with .match(n)
        @param limit: Limit the number of matches.  0=unlimited.
        @type limit: int
        '''
        self.matcher = matcher
        self.limit = int(limit) if limit is not None else 0

    def _iter_children(self, node):
        if node is None:
            return
        # Common attributes for child collections
        for name in ('children', 'childNodes', 'childs', 'nodes', 'subnodes', 'subNodes', 'elements'):
            if hasattr(node, name):
                children = getattr(node, name)
                if callable(children):
                    try:
                        children = children()
                    except TypeError:
                        children = None
                if children is not None:
                    try:
                        for ch in children:
                            yield ch
                    except TypeError:
                        pass
                return
        # Fallback: treat node as iterable (but not string/bytes)
        if hasattr(node, '__iter__') and not isinstance(node, (str, bytes)):
            try:
                for ch in node:
                    yield ch
            except TypeError:
                return

    def find(self, node, list):
        count = 0

        def walk(n):
            nonlocal count
            if n is None:
                return True if (self.limit and count >= self.limit) else False

            try:
                is_match = self.matcher.match(n) if hasattr(
                    self.matcher, 'match') else False
            except Exception:
                is_match = False

            if is_match:
                list.append(n)
                count += 1
                if self.limit and count >= self.limit:
                    return True

            for child in self._iter_children(n):
                if self.limit and count >= self.limit:
                    return True
                if walk(child):
                    if self.limit and count >= self.limit:
                        return True
            return False

        walk(node)
