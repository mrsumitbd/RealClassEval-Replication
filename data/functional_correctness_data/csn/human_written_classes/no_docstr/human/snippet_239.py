import re
import copy

class Rename:

    def __init__(self, op=None, name=None, to=None):
        assert op or name, 'Either op or name must be provided'
        assert not (op and name), 'Either op or name should be provided, but not both'
        assert bool(to), 'The to parameter is required'
        self.to = to
        self.op = re.compile(op) if op else None
        self.name = re.compile(name) if name else None

    def apply(self, graph):
        graph = copy.deepcopy(graph)
        for node in graph.nodes.values():
            if self.op:
                node.op = self.op.sub(self.to, node.op)
            if self.name:
                node.name = self.name.sub(self.to, node.name)
        return graph