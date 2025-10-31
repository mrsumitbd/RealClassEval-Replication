
class DistanceData:

    def __init__(self, names, result):
        self.names = names
        self.result = result

    @property
    def distance(self):
        return self.result

    def index(self, name):
        return self.names.index(name)

    def point(self, name):
        return self.result[self.index(name)]
