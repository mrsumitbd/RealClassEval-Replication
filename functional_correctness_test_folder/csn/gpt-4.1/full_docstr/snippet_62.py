
import threading
import time


class ReadWriteLock:
    '''Read-Write lock class. See docstring in skeleton.'''

    def __init__(self):
        self._lock = threading.RLock()
        self._readers_ok = threading.Condition(self._lock)
        self._writers_ok = threading.Condition(self._lock)
        self._readers = {}  # thread_id -> count
        self._writer = None  # thread_id of current writer
        self._writer_count = 0  # reentrant write lock count
        self._waiting_writers = 0
        self._upgrading = None  # thread_id of upgrading reader

    def _get_thread_id(self):
        return threading.get_ident()

    def acquire_read(self, *, timeout=None):
        me = self._get_thread_id()
        with self._lock:
            start = time.monotonic()
            while True:
                # If I already hold the write lock, allow reentrant read
                if self._writer == me:
                    self._readers[me] = self._readers.get(me, 0) + 1
                    return
                # If no writer, and either no waiting writers or I'm already a reader, allow read
                if (self._writer is None and
                        (self._waiting_writers == 0 or me in self._readers)):
                    self._readers[me] = self._readers.get(me, 0) + 1
                    return
                # Otherwise, must wait
                if timeout is not None:
                    now = time.monotonic()
                    remaining = timeout - (now - start)
                    if remaining <= 0:
                        raise RuntimeError(
                            "Timeout while waiting for read lock")
                    self._readers_ok.wait(remaining)
                else:
                    self._readers_ok.wait()

    def acquire_write(self, *, timeout=None):
        me = self._get_thread_id()
        with self._lock:
            start = time.monotonic()
            # Upgrade: if I'm a reader and no other readers, allow upgrade
            if self._writer == me:
                # Reentrant write lock
                self._writer_count += 1
                return
            if me in self._readers:
                # Only allow one thread to upgrade at a time
                if self._upgrading is not None and self._upgrading != me:
                    raise ValueError("Deadlock: another thread is upgrading")
                self._upgrading = me
            self._waiting_writers += 1
            try:
                while True:
                    # If no readers (except possibly myself) and no writer, allow write
                    readers = set(self._readers.keys())
                    if self._writer is None and (not readers or readers == {me}):
                        self._writer = me
                        self._writer_count = 1
                        # If upgrading, remove my read locks
                        if me in self._readers:
                            del self._readers[me]
                            self._upgrading = None
                        return
                    # If I'm upgrading, but other readers exist, must wait
                    # If another writer, must wait
                    if timeout is not None:
                        now = time.monotonic()
                        remaining = timeout - (now - start)
                        if remaining <= 0:
                            raise RuntimeError(
                                "Timeout while waiting for write lock")
                        self._writers_ok.wait(remaining)
                    else:
                        self._writers_ok.wait()
            finally:
                self._waiting_writers -= 1
                if self._upgrading == me and self._writer == me:
                    self._upgrading = None

    def release(self):
        me = self._get_thread_id()
        with self._lock:
            # Release write lock if held
            if self._writer == me:
                self._writer_count -= 1
                if self._writer_count == 0:
                    self._writer = None
                    # Wake up writers first (writer preference)
                    self._writers_ok.notify_all()
                    self._readers_ok.notify_all()
                return
            # Release read lock if held
            if me in self._readers:
                self._readers[me] -= 1
                if self._readers[me] == 0:
                    del self._readers[me]
                # If no more readers, wake up writers
                if not self._readers:
                    self._writers_ok.notify_all()
                return
            raise ValueError("Current thread does not hold a lock")
