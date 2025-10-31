class PathFinder:
    """Using the a* algorithm we will try to find the best path between two
       points.
    """

    def __init__(self):
        pass

    @staticmethod
    def find(height_map, source, destination):
        sx, sy = source
        dx, dy = destination
        path = []
        height, width = height_map.shape
        graph = height_map.flatten('C')
        pathfinder = AStar(SQMapHandler(graph, width, height))
        start = SQLocation(sx, sy)
        end = SQLocation(dx, dy)
        p = pathfinder.find_path(start, end)
        if not p:
            return path
        for node in p.nodes:
            path.append([node.location.x, node.location.y])
        return path