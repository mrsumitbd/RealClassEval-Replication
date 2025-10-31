class PlateContainer:

    def __init__(self, rotation: dict, **kwargs):
        self.rotation = rotation
        self.status = 'idle'

    def get_rotation(self):
        return self.rotation