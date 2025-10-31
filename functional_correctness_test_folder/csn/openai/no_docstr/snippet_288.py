
import uuid
import copy


class Aspect:
    def __init__(self, id=None):
        self.id = id or uuid.uuid4()

    def getId(self):
        return self.id

    def clone(self):
        return copy.deepcopy(self)
