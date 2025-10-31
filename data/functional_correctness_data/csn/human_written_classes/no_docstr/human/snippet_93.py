class GBObjs:

    def __init__(self, core):
        self._core = core
        self._obj = core._native.video.oam.obj

    def __len__(self):
        return 40

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError()
        sprite = GBSprite(self._obj[index], self._core)
        sprite.constitute(self._core.tiles[0], 0)
        return sprite