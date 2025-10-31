
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
        if self.limit > 0 and len(list) >= self.limit:
            return
        if self.matcher.match(node):
            list.append(node)
        for child in getattr(node, 'children', []):
            self.find(child, list)
