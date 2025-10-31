class Path:
    """ A path object, containing the nodes and total cost."""

    def __init__(self, nodes, total_cost):
        self.nodes = nodes
        self.totalCost = total_cost

    def get_nodes(self):
        return self.nodes

    def get_total_movement_cost(self):
        return self.totalCost