
class Aspect:

    def getId(self):
        return id(self)

    def clone(self):
        return Aspect()
