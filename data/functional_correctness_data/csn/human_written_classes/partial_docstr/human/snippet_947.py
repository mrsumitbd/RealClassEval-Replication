class FontMeta:
    """Font metadata"""

    def __init__(self, meta):
        self._meta = meta
        self.characters = self._meta['characters']
        self.character_ranges = self._meta['character_ranges']
        self.character_height = self._meta['character_height']
        self.character_width = self._meta['character_width']
        self.atlas_height = self._meta['atlas_height']
        self.atlas_width = self._meta['atlas_width']

    @property
    def char_aspect_wh(self):
        return self.character_width / self.character_height

    def char_aspect_hw(self):
        return self.character_height / self.character_width