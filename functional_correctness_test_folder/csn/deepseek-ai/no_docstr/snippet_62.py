
import threading
import time


class ReadWriteLock:

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0
        self._writer = False
        self._pending_writers = 0

    def acquire_read(self, *, timeout=None):
        if timeout is not None and timeout <= 0:
            if not self._read_ready.acquire(blocking=False):
                raise RuntimeError("Could not acquire read lock immediately")
        else:
            if not self._read_ready.acquire(timeout=timeout):
                raise RuntimeError("Timeout expired while acquiring read lock")
        try:
            while self._writer or self._pending_writers > 0:
                if not self._read_ready.wait(timeout=timeout):
                    raise RuntimeError(
                        "Timeout expired while acquiring read lock")
            self._readers += 1
        finally:
            self._read_ready.release()

    def acquire_write(self, *, timeout=None):
        self._pending_writers += 1
        try:
            if timeout is not None and timeout <= 0:
                if not self._read_ready.acquire(blocking=False):
                    raise RuntimeError(
                        "Could not acquire write lock immediately")
            else:
                if not self._read_ready.acquire(timeout=timeout):
                    raise RuntimeError(
                        "Timeout expired while acquiring write lock")
            try:
                while self._readers > 0 or self._writer:
                    if not self._read_ready.wait(timeout=timeout):
                        raise RuntimeError(
                            "Timeout expired while acquiring write lock")
                self._writer = True
            except:
                self._read_ready.release()
                raise
        finally:
            self._pending_writers -= 1

    def release(self):
        self._read_ready.acquire()
        try:
            if self._writer:
                self._writer = False
            else:
                if self._readers <= 0:
                    raise RuntimeError(
                        "No active read or write lock to release")
                self._readers -= 1
            self._read_ready.notify_all()
        finally:
            self._read_ready.release()
