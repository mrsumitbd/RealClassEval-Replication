
class Aspect:

    def __init__(self, id):
        self.id = id

    def getId(self):
        return self.id

    def clone(self):
        return Aspect(self.id)
