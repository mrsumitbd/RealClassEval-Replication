
class Aspect:

    def __init__(self, aspect_id):
        self.aspect_id = aspect_id

    def getId(self):
        return self.aspect_id

    def clone(self):
        return Aspect(self.aspect_id)
