
import threading
import time


class ReadWriteLock:
    '''Read-Write lock class. See docstring in skeleton.'''

    def __init__(self):
        self._cond = threading.Condition(threading.RLock())
        self._readers = {}  # thread_id -> count
        self._writer = None  # thread_id of current writer
        self._writer_count = 0  # reentrant write lock count
        self._waiting_writers = 0
        self._upgrading = None  # thread_id of upgrading reader

    def acquire_read(self, *, timeout=None):
        me = threading.get_ident()
        with self._cond:
            # If this thread is the writer, allow reentrant read
            if self._writer == me:
                self._readers[me] = self._readers.get(me, 0) + 1
                return

            # If this thread is already a reader, allow reentrant read
            if me in self._readers:
                self._readers[me] += 1
                return

            # Wait until: no writer, and no waiting writers (writer preference)
            endtime = None
            if timeout is not None:
                if timeout <= 0:
                    endtime = time.monotonic()
                else:
                    endtime = time.monotonic() + timeout

            while True:
                if self._writer is None and self._waiting_writers == 0:
                    self._readers[me] = 1
                    return
                # If this thread is a reader, allow reentrant read
                if me in self._readers:
                    self._readers[me] += 1
                    return
                # If timeout expired
                if timeout is not None:
                    now = time.monotonic()
                    remaining = endtime - now
                    if remaining <= 0:
                        raise RuntimeError(
                            "Timeout while waiting for read lock")
                    self._cond.wait(remaining)
                else:
                    self._cond.wait()

    def acquire_write(self, *, timeout=None):
        me = threading.get_ident()
        with self._cond:
            # Reentrant write lock
            if self._writer == me:
                self._writer_count += 1
                return

            # Upgrade: if this thread is a reader, and no other readers
            if me in self._readers:
                if self._upgrading is not None and self._upgrading != me:
                    raise ValueError(
                        "Another thread is already upgrading from read to write")
                if len(self._readers) > 1:
                    # Other readers present, can't upgrade
                    endtime = None
                    if timeout is not None:
                        if timeout <= 0:
                            endtime = time.monotonic()
                        else:
                            endtime = time.monotonic() + timeout
                    self._upgrading = me
                    try:
                        while len(self._readers) > 1 or self._writer is not None:
                            if timeout is not None:
                                now = time.monotonic()
                                remaining = endtime - now
                                if remaining <= 0:
                                    raise RuntimeError(
                                        "Timeout while waiting for write lock upgrade")
                                self._cond.wait(remaining)
                            else:
                                self._cond.wait()
                    finally:
                        self._upgrading = None
                # Now, only this thread is a reader and no writer
                self._writer = me
                self._writer_count = 1
                del self._readers[me]
                return

            # Normal write lock acquisition
            self._waiting_writers += 1
            endtime = None
            if timeout is not None:
                if timeout <= 0:
                    endtime = time.monotonic()
                else:
                    endtime = time.monotonic() + timeout
            try:
                while self._writer is not None or len(self._readers) > 0:
                    if timeout is not None:
                        now = time.monotonic()
                        remaining = endtime - now
                        if remaining <= 0:
                            raise RuntimeError(
                                "Timeout while waiting for write lock")
                        self._cond.wait(remaining)
                    else:
                        self._cond.wait()
                self._writer = me
                self._writer_count = 1
            finally:
                self._waiting_writers -= 1

    def release(self):
        me = threading.get_ident()
        with self._cond:
            # Release write lock
            if self._writer == me:
                self._writer_count -= 1
                if self._writer_count == 0:
                    self._writer = None
                    self._cond.notify_all()
                return

            # Release read lock
            if me in self._readers:
                self._readers[me] -= 1
                if self._readers[me] == 0:
                    del self._readers[me]
                    self._cond.notify_all()
                return

            raise ValueError("Current thread does not hold a lock")
