
class DistanceData:

    def __init__(self, names, result):
        self._names = list(names)
        self._result = [list(row) for row in result]
        self._name_to_index = {name: i for i, name in enumerate(self._names)}

    @property
    def distance(self):
        return [row[:] for row in self._result]

    def index(self, name):
        return self._name_to_index[name]

    def point(self, name):
        idx = self.index(name)
        return self._result[idx][:]
