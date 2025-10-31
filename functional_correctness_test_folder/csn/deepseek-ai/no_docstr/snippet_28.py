
class DistanceData:

    def __init__(self, names, result):
        self._names = names
        self._result = result

    @property
    def distance(self):
        return self._result

    def index(self, name):
        return self._names.index(name)

    def point(self, name):
        return self._result[self.index(name)]
