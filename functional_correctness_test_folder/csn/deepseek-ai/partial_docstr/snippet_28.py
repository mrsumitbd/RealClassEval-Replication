
class DistanceData:

    def __init__(self, names, result):
        self._names = names
        self._result = result

    @property
    def distance(self):
        return self._result.min_distance

    def index(self, name):
        idx = self._names.index(name)
        if idx == 0:
            return self._result.b1
        else:
            return self._result.b2

    def point(self, name):
        idx = self._names.index(name)
        if idx == 0:
            return self._result.nearest_points[0]
        else:
            return self._result.nearest_points[1]
