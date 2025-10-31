import threading
import time
from collections import defaultdict


class ReadWriteLock:

    def __init__(self):
        self._cond = threading.Condition()
        self._readers = defaultdict(int)  # thread_id -> count
        self._writer = None               # thread_id or None
        self._writer_count = 0
        self._waiting_writers = 0

    def _tid(self):
        return threading.get_ident()

    def _can_acquire_read(self, tid):
        # Allow read if no active writer and either no waiting writers
        # or the thread already holds a read lock (reentrant read).
        if self._writer is not None:
            return False
        if self._waiting_writers > 0 and self._readers.get(tid, 0) == 0:
            return False
        return True

    def _can_acquire_write(self, tid):
        # Allow write if no other writer and no readers (or reentrant write)
        if self._writer is None:
            return len(self._readers) == 0
        return self._writer == tid  # reentrant write

    def acquire_read(self, *, timeout=None):
        tid = self._tid()
        # Non-blocking check
        if timeout is not None and timeout <= 0:
            with self._cond:
                if self._can_acquire_read(tid):
                    self._readers[tid] += 1
                    return
                raise RuntimeError("Timed out acquiring read lock")
        # Blocking with optional timeout
        deadline = None if timeout is None else (time.monotonic() + timeout)
        with self._cond:
            while not self._can_acquire_read(tid):
                if deadline is None:
                    self._cond.wait()
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise RuntimeError("Timed out acquiring read lock")
                    self._cond.wait(remaining)
            self._readers[tid] += 1

    def acquire_write(self, *, timeout=None):
        tid = self._tid()
        with self._cond:
            # Deadlock condition: cannot upgrade from read to write
            if self._readers.get(tid, 0) > 0 and self._writer != tid:
                raise ValueError(
                    "Deadlock risk: cannot acquire write while holding read lock")
        # Non-blocking check
        if timeout is not None and timeout <= 0:
            with self._cond:
                if self._can_acquire_write(tid):
                    if self._writer == tid:
                        self._writer_count += 1
                    else:
                        self._writer = tid
                        self._writer_count = 1
                    return
                raise RuntimeError("Timed out acquiring write lock")
        deadline = None if timeout is None else (time.monotonic() + timeout)
        waiting_marked = False
        with self._cond:
            if self._writer != tid:
                self._waiting_writers += 1
                waiting_marked = True
            try:
                while not self._can_acquire_write(tid):
                    if deadline is None:
                        self._cond.wait()
                    else:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise RuntimeError(
                                "Timed out acquiring write lock")
                        self._cond.wait(remaining)
                if self._writer == tid:
                    self._writer_count += 1
                else:
                    self._writer = tid
                    self._writer_count = 1
            finally:
                if waiting_marked:
                    self._waiting_writers -= 1

    def release(self):
        tid = self._tid()
        with self._cond:
            if self._writer == tid and self._writer_count > 0:
                self._writer_count -= 1
                if self._writer_count == 0:
                    self._writer = None
                    self._cond.notify_all()
                return
            rc = self._readers.get(tid, 0)
            if rc > 0:
                if rc == 1:
                    del self._readers[tid]
                else:
                    self._readers[tid] = rc - 1
                if len(self._readers) == 0:
                    self._cond.notify_all()
                return
            raise RuntimeError("Current thread does not hold the lock")
