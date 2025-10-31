
class patch_obj:

    def __init__(self):
        self._data = None

    def __str__(self):
        return str(self._data) if self._data is not None else "patch_obj"
