class _GetchWindows:

    def __init__(self):
        import msvcrt
        self.keymap = {b'G': b'\x01', b'K': b'\x02', b'S': b'\x04', b'O': b'\x05', b'M': b'\x06', b'P': b'\x0e', b'H': b'\x10'}

    def __call__(self):
        import msvcrt
        ch = msvcrt.getch()
        if ch == b'\xe0':
            ch = msvcrt.getch()
            if ch in self.keymap:
                ch = self.keymap[ch]
        return ch