class KeyEntry:

    def __init__(self, keycode, mask):
        self.keycode = keycode
        self.mask = mask

    def __repr__(self):
        return f'KeyEntry({self.keycode}, {self.mask})'

    def __eq__(self, rval):
        return self.keycode == rval.keycode and self.mask == rval.mask