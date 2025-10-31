
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
        self.limit = limit

    def find(self, node, list):
        '''
        Traverse the tree looking for matches.
        @param node: A node to match on.
        @type node: L{SchemaObject}
        @param list: A list to fill.
        @type list: list
        '''
        # Stop if we already reached the limit
        if self.limit and len(list) >= self.limit:
            return

        # Check current node
        try:
            if self.matcher.match(node):
                list.append(node)
                if self.limit and len(list) >= self.limit:
                    return
        except Exception:
            # If matcher raises, ignore this node
            pass

        # Recurse into children if any
        children = None
        if hasattr(node, 'children'):
            children = node.children
        elif hasattr(node, 'subnodes'):
            children = node.subnodes
        elif hasattr(node, 'elements'):
            children = node.elements
        else:
            # Try to iterate directly
            try:
                for _ in node:
                    pass
                children = node
            except TypeError:
                children = None

        if children:
            for child in children:
                self.find(child, list)
