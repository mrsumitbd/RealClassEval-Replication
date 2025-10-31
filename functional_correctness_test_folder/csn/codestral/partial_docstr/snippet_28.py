
class DistanceData:

    def __init__(self, names, result):
        self.names = names
        self.result = result

    @property
    def distance(self):
        return self.result.min_distance

    def index(self, name):
        if name == self.names[0]:
            return self.result.nearest_points[0].face
        elif name == self.names[1]:
            return self.result.nearest_points[1].face
        else:
            raise ValueError(f"Name {name} not found in {self.names}")

    def point(self, name):
        if name == self.names[0]:
            return self.result.nearest_points[0].point
        elif name == self.names[1]:
            return self.result.nearest_points[1].point
        else:
            raise ValueError(f"Name {name} not found in {self.names}")
