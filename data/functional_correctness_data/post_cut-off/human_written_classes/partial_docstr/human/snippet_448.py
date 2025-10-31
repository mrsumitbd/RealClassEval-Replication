import threading

class TeeOutput:
    """Thread-safe output duplicator to both terminal and log file"""

    def __init__(self, stream, log_file):
        self.terminal = stream
        self.log = open(log_file, 'a', encoding='utf-8', buffering=1)
        self.lock = threading.Lock()

    def write(self, message):
        with self.lock:
            self.terminal.write(message)
            self.terminal.flush()
            try:
                self.log.write(message)
                self.log.flush()
            except (ValueError, OSError):
                pass

    def flush(self):
        with self.lock:
            self.terminal.flush()
            try:
                self.log.flush()
            except (ValueError, OSError):
                pass

    def close(self):
        with self.lock:
            try:
                self.log.close()
            except:
                pass

    def fileno(self):
        return self.terminal.fileno()

    def isatty(self):
        return self.terminal.isatty()