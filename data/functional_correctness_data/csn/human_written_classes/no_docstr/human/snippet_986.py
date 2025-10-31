class DisplayList:

    def __init__(self):
        self._rows = []

    def add(self, key, val):
        self._rows.append(tuple((key, val)))

    def print(self, _format, clear=False, **kwargs):
        k_width = max([len(k) for k, v in self._rows if k])
        for k, v in self._rows:
            if k:
                print(_format.format(k=k.ljust(k_width), v=v, **kwargs))
        if clear:
            self.clear()

    def clear(self):
        self._rows.clear()