
import threading
import time
import sys


class ReadWriteLock:
    """
    A simple read–write lock that allows multiple readers or a single writer.
    New readers are blocked if a writer is waiting to avoid writer starvation.
    """

    def __init__(self):
        self._cond = threading.Condition(threading.Lock())
        self._readers = 0          # number of active readers
        self._writer = None        # thread id of the active writer
        self._waiting_writers = 0  # number of writers waiting
        # Per‑thread ownership data for re‑entrancy
        self._owner = None         # thread id that owns the lock
        self._owner_type = None    # 'read' or 'write'
        self._owner_count = 0      # re‑entrancy count

    def _now(self):
        return time.monotonic()

    def acquire_read(self, *, timeout=None):
        """Acquire a read lock for the current thread."""
        tid = threading.get_ident()
        with self._cond:
            # Re‑entrant read acquisition
            if self._owner == tid and self._owner_type == 'read':
                self._owner_count += 1
                return

            # Deadlock detection: writer already holds lock
            if self._owner == tid and self._owner_type == 'write':
                # Writer can read; allow re‑entrancy
                self._owner_count += 1
                return

            # Non‑blocking check
            if timeout is not None and timeout <= 0:
                if self._writer is not None or self._waiting_writers > 0:
                    raise RuntimeError(
                        "Read lock not available (non‑blocking)")
                # Acquire immediately
                self._readers += 1
                self._owner = tid
                self._owner_type = 'read'
                self._owner_count = 1
                return

            # Blocking or timed wait
            end = None if timeout is None else self._now() + timeout
            while True:
                if self._writer is None and self._waiting_writers == 0:
                    # No writer active or waiting
                    self._readers += 1
                    self._owner = tid
                    self._owner_type = 'read'
                    self._owner_count = 1
                    return
                if timeout is not None:
                    remaining = end - self._now()
                    if remaining <= 0:
                        raise RuntimeError("Read lock acquisition timed out")
                    self._cond.wait(remaining)
                else:
                    self._cond.wait()

    def acquire_write(self, *, timeout=None):
        """Acquire a write lock for the current thread."""
        tid = threading.get_ident()
        with self._cond:
            # Re‑entrant write acquisition
            if self._owner == tid and self._owner_type == 'write':
                self._owner_count += 1
                return

            # Deadlock detection: thread holds read lock
            if self._owner == tid and self._owner_type == 'read':
                raise ValueError(
                    "Deadlock: thread holds read lock and requests write lock")

            # Non‑blocking check
            if timeout is not None and timeout <= 0:
                if self._writer is not None or self._readers > 0:
                    raise RuntimeError(
                        "Write lock not available (non‑blocking)")
                # Acquire immediately
                self._writer = tid
                self._owner = tid
                self._owner_type = 'write'
                self._owner_count = 1
                return

            # Blocking or timed wait
            self._waiting_writers += 1
            end = None if timeout is None else self._now() + timeout
            try:
                while True:
                    if self._writer is None and self._readers == 0:
                        # No active readers or writer
                        self._writer = tid
                        self._owner = tid
                        self._owner_type = 'write'
                        self._owner_count = 1
                        return
                    if timeout is not None:
                        remaining = end - self._now()
                        if remaining <= 0:
                            raise RuntimeError(
                                "Write lock acquisition timed out")
                        self._cond.wait(remaining)
                    else:
                        self._cond.wait()
            finally:
                self._waiting_writers -= 1

    def release(self):
        """Release the lock held by the current thread."""
        tid = threading.get_ident()
        with self._cond:
            if self._owner != tid:
                raise RuntimeError("Current thread does not hold the lock")

            self._owner_count -= 1
            if self._owner_count > 0:
                return  # still holds lock re‑entrantly

            # Fully release
            if self._owner_type == 'read':
                self._readers -= 1
                if self._readers == 0:
                    self._owner = None
                    self._owner_type = None
            elif self._owner_type == 'write':
                self._writer = None
                self._owner = None
                self._owner_type = None
            else:
                raise RuntimeError("Unknown lock type")

            self._cond.notify_all()
