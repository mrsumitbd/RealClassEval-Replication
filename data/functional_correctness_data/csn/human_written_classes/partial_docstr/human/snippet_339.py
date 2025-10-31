class SQMapHandler:
    """A simple Square Map implementation"""

    def __init__(self, map_data, width, height):
        self.m = map_data
        self.w = width
        self.h = height

    def get_node(self, location):
        x = location.x
        y = location.y
        if x < 0 or x >= self.w or y < 0 or (y >= self.h):
            return None
        d = self.m[y * self.w + x]
        return Node(location, d, y * self.w + x)

    def get_adjacent_nodes(self, cur_node, destination):
        result = []
        cl = cur_node.location
        dl = destination
        n = self._handle_node(cl.x + 1, cl.y, cur_node, dl.x, dl.y)
        if n:
            result.append(n)
        n = self._handle_node(cl.x - 1, cl.y, cur_node, dl.x, dl.y)
        if n:
            result.append(n)
        n = self._handle_node(cl.x, cl.y + 1, cur_node, dl.x, dl.y)
        if n:
            result.append(n)
        n = self._handle_node(cl.x, cl.y - 1, cur_node, dl.x, dl.y)
        if n:
            result.append(n)
        return result

    def _handle_node(self, x, y, from_node, destination_x, destination_y):
        n = self.get_node(SQLocation(x, y))
        if n is not None:
            dx = max(x, destination_x) - min(x, destination_x)
            dy = max(y, destination_y) - min(y, destination_y)
            em_cost = dx + dy
            n.mCost += from_node.mCost
            n.score = n.mCost + em_cost
            n.parent = from_node
            return n
        return None