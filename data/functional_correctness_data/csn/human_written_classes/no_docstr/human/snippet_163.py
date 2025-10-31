class PmlMaxHeightMixIn:

    def setMaxHeight(self, availHeight: int) -> int:
        self.availHeightValue: int = availHeight
        if availHeight < 70000 and hasattr(self, 'canv'):
            if not hasattr(self.canv, 'maxAvailHeightValue'):
                self.canv.maxAvailHeightValue = 0
            self.availHeightValue = self.canv.maxAvailHeightValue = max(availHeight, self.canv.maxAvailHeightValue)
        return self.availHeightValue

    def getMaxHeight(self) -> int:
        return self.availHeightValue if hasattr(self, 'availHeightValue') else 0