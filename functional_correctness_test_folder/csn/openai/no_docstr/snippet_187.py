
class NodeFinder:
    def __init__(self, matcher, limit=0):
        """
        Create a NodeFinder.

        Parameters
        ----------
        matcher : callable
            A function that receives a node and returns ``True`` if the node
            matches the desired condition.
        limit : int, optional
            Maximum number of matches to collect. 0 means no limit.
        """
        self.matcher = matcher
        self.limit = limit

    def find(self, node, result):
        """
        Recursively search *node* and its descendants, appending matching nodes
        to *result*.

        Parameters
        ----------
        node : any
            The root node to start searching from.
        result : list
            A list that will be populated with matching nodes.
        """
        # Stop if we already reached the limit
        if self.limit and len(result) >= self.limit:
            return

        # Check the current node
        try:
            if self.matcher(node):
                result.append(node)
                if self.limit and len(result) >= self.limit:
                    return
        except Exception:
            # If matcher raises, ignore this node
            pass

        # Determine children of the node
        children = None
        if hasattr(node, "children"):
            children = node.children
        elif hasattr(node, "childNodes"):
            children = node.childNodes
        elif hasattr(node, "getchildren"):
            try:
                children = node.getchildren()
            except Exception:
                children = None
        elif isinstance(node, (list, tuple)):
            children = node
        else:
            # Try to iterate over the node if it is iterable
            try:
                children = list(node)
            except Exception:
                children = None

        # Recurse into children
        if children:
            for child in children:
                if self.limit and len(result) >= self.limit:
                    break
                self.find(child, result)
