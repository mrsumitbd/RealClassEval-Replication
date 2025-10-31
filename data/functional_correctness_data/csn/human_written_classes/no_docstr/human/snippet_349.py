import threading
import re

class DebugLogBuffer:

    def __init__(self, log):
        self.buf = []
        self.first = True
        self.linebreak_re = re.compile(b'.*\n')
        self.log = log
        self.lock = threading.Lock()

    def __call__(self, c):
        with self.lock:
            self._process(c)

    def _process(self, c):
        if c is None:
            text = b''.join(self.buf)
            del self.buf[:]
        elif b'\n' in c:
            m = self.linebreak_re.match(c)
            j = m.end()
            self.buf.append(c[:j])
            text = b''.join(self.buf)
            self.buf[:] = [c[j:]]
        else:
            self.buf.append(c)
            return
        text = text.decode('utf-8', 'replace')
        if text.endswith('\n'):
            text = text[:-1]
        if text:
            if self.first:
                self.log.debug('OUTPUT -------->', continued=True)
                self.first = False
            self.log.debug(text, continued=True)