
class NodeFinder:

    def __init__(self, matcher, limit=0):
        """
        Initialize the NodeFinder with a matcher function and an optional limit.

        Args:
            matcher (function): A function that takes a node and returns True if it matches the desired condition.
            limit (int, optional): The maximum number of matches to return. Defaults to 0, which means no limit.
        """
        self.matcher = matcher
        self.limit = limit

    def find(self, node, lst):
        """
        Find nodes in the given list that match the condition specified by the matcher function.

        Args:
            node (any): The current node being processed (not used in this implementation).
            lst (list): The list of nodes to search.

        Returns:
            list: A list of nodes that match the condition.
        """
        matches = []
        for n in lst:
            if self.matcher(n):
                matches.append(n)
                if self.limit > 0 and len(matches) >= self.limit:
                    break
        return matches
