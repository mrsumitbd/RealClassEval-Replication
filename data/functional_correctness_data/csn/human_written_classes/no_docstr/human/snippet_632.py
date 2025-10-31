from ufo2ft.fontInfoData import getAttrWithFallback

class _LazyFontName:

    def __init__(self, font):
        self.font = font

    def __str__(self):
        return getAttrWithFallback(self.font.info, 'postscriptFontName')