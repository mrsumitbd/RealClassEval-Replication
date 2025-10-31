import threading
import time


class ReadWriteLock:
    '''Read-Write lock class. A read-write lock differs from a standard
    threading.RLock() by allowing multiple threads to simultaneously hold a
    read lock, while allowing only a single thread to hold a write lock at the
    same point of time.
    When a read lock is requested while a write lock is held, the reader
    is blocked; when a write lock is requested while another write lock is
    held or there are read locks, the writer is blocked.
    Writers are always preferred by this implementation: if there are blocked
    threads waiting for a write lock, current readers may request more read
    locks (which they eventually should free, as they starve the waiting
    writers otherwise), but a new thread requesting a read lock will not
    be granted one, and block. This might mean starvation for readers if
    two writer threads interweave their calls to acquire_write() without
    leaving a window only for readers.
    In case a current reader requests a write lock, this can and will be
    satisfied without giving up the read locks first, but, only one thread
    may perform this kind of lock upgrade, as a deadlock would otherwise
    occur. After the write lock has been granted, the thread will hold a
    full write lock, and not be downgraded after the upgrading call to
    acquire_write() has been match by a corresponding release().
    '''

    def __init__(self):
        '''Initialize this read-write lock.'''
        self._mutex = threading.RLock()
        self._cond = threading.Condition(self._mutex)
        self._readers = {}  # tid -> count
        self._readers_count = 0
        self._writer_tid = None
        self._writer_count = 0
        self._waiting_writers = 0
        self._upgrading_tid = None

    def _tid(self):
        return threading.get_ident()

    def _get_read_count(self, tid):
        return self._readers.get(tid, 0)

    def _can_read(self, tid):
        # Block if another writer active
        if self._writer_tid is not None and self._writer_tid != tid:
            return False
        # Prefer writers: if there are waiting writers, only existing readers may reenter
        if self._waiting_writers > 0 and self._get_read_count(tid) == 0 and self._writer_tid is None:
            return False
        # If an upgrade is in progress by another thread, block new readers to allow upgrade to proceed
        if self._upgrading_tid is not None and self._upgrading_tid != tid and self._writer_tid is None:
            # Existing readers can reenter
            if self._get_read_count(tid) == 0:
                return False
        return True

    def _can_acquire_write_plain(self):
        return (self._writer_tid is None) and (self._readers_count == 0)

    def acquire_read(self, *, timeout=None):
        '''Acquire a read lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.
        In case timeout is None, the call to acquire_read blocks until the
        lock request can be serviced.
        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown.'''
        tid = self._tid()
        with self._cond:
            # Fast path if allowed
            if self._can_read(tid):
                self._readers[tid] = self._get_read_count(tid) + 1
                self._readers_count += 1
                return

            # Non-blocking path
            if timeout is not None and timeout <= 0:
                raise RuntimeError("Timeout acquiring read lock")

            end = None if timeout is None else (time.monotonic() + timeout)
            while not self._can_read(tid):
                remaining = None if end is None else (end - time.monotonic())
                if remaining is not None and remaining <= 0:
                    raise RuntimeError("Timeout acquiring read lock")
                self._cond.wait(remaining)

            self._readers[tid] = self._get_read_count(tid) + 1
            self._readers_count += 1

    def acquire_write(self, *, timeout=None):
        '''Acquire a write lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.
        In case the write lock cannot be serviced due to the deadlock
        condition mentioned above, a ValueError is raised.
        In case timeout is None, the call to acquire_write blocks until the
        lock request can be serviced.
        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown.'''
        tid = self._tid()
        with self._cond:
            # Re-entrant write acquisition
            if self._writer_tid == tid:
                self._writer_count += 1
                return

            # Upgrade path if thread currently holds read locks
            my_read_count = self._get_read_count(tid)
            if my_read_count > 0:
                # Deadlock prevention: only one upgrader allowed
                if self._upgrading_tid is not None and self._upgrading_tid != tid:
                    raise ValueError(
                        "Deadlock risk: another thread is upgrading read to write")
                # Non-blocking immediate check
                if timeout is not None and timeout <= 0:
                    # Can upgrade immediately only if no other readers and no other writer
                    if self._writer_tid is None and (self._readers_count == my_read_count):
                        self._upgrading_tid = tid
                        # Convert upgrade
                        self._writer_tid = tid
                        self._writer_count = 1
                        # Remove our read locks (no downgrade after release)
                        self._readers_count -= my_read_count
                        if my_read_count > 0:
                            self._readers.pop(tid, None)
                        self._upgrading_tid = None
                        return
                    else:
                        raise RuntimeError(
                            "Timeout acquiring write lock (upgrade)")
                # Blocking/timeout upgrade
                end = None if timeout is None else (time.monotonic() + timeout)
                # Mark as upgrading and prefer writers
                if self._upgrading_tid is None:
                    self._upgrading_tid = tid
                self._waiting_writers += 1
                try:
                    while not (self._writer_tid is None and self._readers_count == my_read_count):
                        remaining = None if end is None else (
                            end - time.monotonic())
                        if remaining is not None and remaining <= 0:
                            raise RuntimeError(
                                "Timeout acquiring write lock (upgrade)")
                        self._cond.wait(remaining)
                    # Convert upgrade
                    self._writer_tid = tid
                    self._writer_count = 1
                    # Remove our read locks to avoid downgrade after write release
                    self._readers_count -= my_read_count
                    if my_read_count > 0:
                        self._readers.pop(tid, None)
                finally:
                    self._upgrading_tid = None
                    self._waiting_writers -= 1
                return

            # Plain write acquisition (no current read locks)
            if timeout is not None and timeout <= 0:
                if self._can_acquire_write_plain():
                    self._writer_tid = tid
                    self._writer_count = 1
                    return
                else:
                    raise RuntimeError("Timeout acquiring write lock")

            end = None if timeout is None else (time.monotonic() + timeout)
            self._waiting_writers += 1
            try:
                while not self._can_acquire_write_plain():
                    remaining = None if end is None else (
                        end - time.monotonic())
                    if remaining is not None and remaining <= 0:
                        raise RuntimeError("Timeout acquiring write lock")
                    self._cond.wait(remaining)
                self._writer_tid = tid
                self._writer_count = 1
            finally:
                self._waiting_writers -= 1

    def release(self):
        '''Release the currently held lock.
        In case the current thread holds no lock, a ValueError is thrown.'''
        tid = self._tid()
        with self._cond:
            if self._writer_tid == tid and self._writer_count > 0:
                self._writer_count -= 1
                if self._writer_count == 0:
                    self._writer_tid = None
                    # Wake up all: writers first (due to waiting_writers preference enforced in acquire)
                    self._cond.notify_all()
                else:
                    # Still holds write reentrantly; nothing else to do
                    pass
                return

            rc = self._get_read_count(tid)
            if rc > 0:
                # Release one read lock
                if rc == 1:
                    self._readers.pop(tid, None)
                else:
                    self._readers[tid] = rc - 1
                self._readers_count -= 1
                if self._readers_count == 0:
                    # Wake up potential writers
                    self._cond.notify_all()
                return

            raise ValueError("Current thread holds no lock to release")
