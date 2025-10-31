from curtsies.fmtfuncs import blue, red, green
from curtsies.formatstring import linesplit

class Connection:

    def __init__(self, sock):
        self.sock = sock
        self.received = []

    def fileno(self):
        return self.sock.fileno()

    def on_read(self):
        self.received.append(self.sock.recv(50))

    def render(self):
        return linesplit(green(''.join((s.decode('latin-1') for s in self.received))), 80) if self.received else ['']