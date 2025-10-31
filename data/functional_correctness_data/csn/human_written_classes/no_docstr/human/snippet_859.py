class _HouseWithIdBuilder:

    def __init__(self):
        self._id = None
        self._name = None
        self._world = None

    def id(self, id: int):
        self._id = id
        return self

    def world(self, world: str):
        self._world = world
        return self

    def name(self, name: str):
        self._name = name
        return self