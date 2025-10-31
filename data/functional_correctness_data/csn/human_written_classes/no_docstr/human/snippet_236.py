class NodePattern:

    def __init__(self, op, condition=None):
        self.op = op
        self.condition = condition

    def match(self, graph, node):
        if isinstance(node, list):
            return ([], None)
        if self.op == node.op:
            following = graph.outgoing(node)
            if len(following) == 1:
                following = following[0]
            return ([node], following)
        else:
            return ([], None)