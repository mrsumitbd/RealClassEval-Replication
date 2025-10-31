class GBAObjs:

    def __init__(self, core):
        self._core = core
        self._obj = core._native.video.oam.obj

    def __len__(self):
        return 128

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError()
        sprite = GBASprite(self._obj[index])
        tiles = self._core.tiles[3 if sprite._256Color else 2]
        map1D = bool(self._core._native.memory.io[0] & 64)
        sprite.constitute(tiles, 0 if map1D else 32)
        return sprite