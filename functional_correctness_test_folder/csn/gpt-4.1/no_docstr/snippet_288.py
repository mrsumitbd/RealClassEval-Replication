
class Aspect:
    def __init__(self, id=None):
        self._id = id

    def getId(self):
        return self._id

    def clone(self):
        return Aspect(self._id)
