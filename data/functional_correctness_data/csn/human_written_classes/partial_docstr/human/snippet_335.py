class Node:
    """ The basic unit/pixel/location is a Node."""

    def __init__(self, location, movement_cost, lid, parent=None):
        self.location = location
        self.mCost = movement_cost
        self.parent = parent
        self.score = 0
        self.lid = lid

    def __eq__(self, n):
        if n.lid == self.lid:
            return 1
        else:
            return 0