import curses

class ostream:

    def __init__(self, fo, caps, extra=None):
        self.fo = fo
        self.caps = caps
        self.extra = extra

    def __lshift__(self, q):
        if isinstance(q, str):
            self.fo.write(q)
        elif isinstance(q, list):
            cmd = q[0]
            args = q[1:]
            if cmd in self.caps:
                self.fo.write(curses.tparm(self.caps[cmd], *args).decode('ascii'))
            elif self.extra and cmd in self.extra:
                self.fo.write(self.extra[cmd](*args))
            else:
                raise RuntimeError('Could not find terminfo code: ' + cmd)
        elif hasattr(q, '__iter__'):
            for item in q:
                self << item
        self.fo.flush()
        return self