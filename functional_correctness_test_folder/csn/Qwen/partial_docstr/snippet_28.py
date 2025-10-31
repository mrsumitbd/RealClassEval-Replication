
class DistanceData:

    def __init__(self, names, result):
        self.names = names
        self.result = result

    @property
    def distance(self):
        return self.result.min_distance

    def index(self, name):
        if name == self.names[0]:
            return self.result.b1
        elif name == self.names[1]:
            return self.result.b2
        else:
            raise ValueError("Name not found in stored names.")

    def point(self, name):
        if name == self.names[0]:
            return self.result.nearest_points[0]
        elif name == self.names[1]:
            return self.result.nearest_points[1]
        else:
            raise ValueError("Name not found in stored names.")
