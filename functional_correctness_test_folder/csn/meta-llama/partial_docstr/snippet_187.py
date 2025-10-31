
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

    def find(self, node, nodes):
        '''
        Find nodes that match the specified criteria.

        @param node: The root node to start searching from.
        @param nodes: A list of nodes to search.
        @return: A list of nodes that match the criteria.
        '''
        matches = []
        for n in nodes:
            if self.matcher.match(n):
                matches.append(n)
                if self.limit > 0 and len(matches) >= self.limit:
                    break
        return matches
