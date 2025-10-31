import atexit
import os

class SingleInstance:

    def __init__(self, lockfile):
        self.lockfile = os.path.abspath(lockfile)
        self.fp = None
        try:
            self.fp = open(self.lockfile, 'w+')
            if os.name == 'nt':
                try:
                    msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
                except OSError:
                    raise RuntimeError('Another instance is already running.')
            else:
                try:
                    fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError:
                    raise RuntimeError('Another instance is already running.')
            self.fp.write(str(os.getpid()))
            self.fp.flush()
            atexit.register(self.cleanup)
        except Exception:
            if self.fp:
                self.fp.close()
            raise

    def cleanup(self):
        try:
            if self.fp:
                self.fp.close()
            if os.path.exists(self.lockfile):
                os.remove(self.lockfile)
        except Exception:
            pass