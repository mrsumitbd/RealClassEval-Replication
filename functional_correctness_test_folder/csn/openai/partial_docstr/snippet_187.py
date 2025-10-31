
class NodeFinder:
    '''
    Find nodes based on flexible criteria.  The I{matcher} is
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

    def find(self, node, result_list):
        """
        Recursively search *node* and its descendants, adding any node
        that satisfies ``self.matcher.match(node)`` to *result_list*.
        The search stops when *self.limit* matches have been found
        (unless *self.limit* is 0, which means unlimited).
        """
        if node is None:
            return

        # Stop if limit reached
        if self.limit and len(result_list) >= self.limit:
            return

        # Check current node
        try:
            if self.matcher.match(node):
                result_list.append(node)
                if self.limit and len(result_list) >= self.limit:
                    return
        except Exception:
            # If matcher raises, ignore this node
            pass

        # Determine children to traverse
        children = None
        if hasattr(node, 'children'):
            children = node.children
        elif isinstance(node, dict):
            children = node.values()
        elif isinstance(node, (list, tuple, set)):
            children = node
        elif hasattr(node, '__iter__') and not isinstance(node, (str, bytes)):
            children = node
        else:
            children = None

        if children:
            for child in children:
                if self.limit and len(result_list) >= self.limit:
                    break
                self.find(child, result_list)
