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
        self._cond = threading.Condition(threading.RLock())
        self._readers = {}  # tid -> count
        self._writer = None
        self._write_count = 0
        self._waiting_writers = 0
        # tid of thread attempting upgrade (reader->writer), at most one
        self._upgrader = None

    def _tid(self):
        return threading.get_ident()

    def _now(self):
        return time.monotonic()

    def _has_other_readers(self, tid):
        # any readers other than tid?
        for t, c in self._readers.items():
            if t != tid and c > 0:
                return True
        return False

    def acquire_read(self, *, timeout=None):
        '''Acquire a read lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.
        In case timeout is None, the call to acquire_read blocks until the
        lock request can be serviced.
        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown.'''
        tid = self._tid()
        with self._cond:
            # Fast path: if this thread already holds the write lock, allow read reentrantly
            if self._writer == tid:
                self._readers[tid] = self._readers.get(tid, 0) + 1
                return

            deadline = None
            if timeout is not None:
                if timeout <= 0:
                    deadline = self._now()  # immediate check
                else:
                    deadline = self._now() + timeout

            while True:
                writer_active = self._writer is not None
                already_reader = self._readers.get(tid, 0) > 0
                writers_waiting = self._waiting_writers > 0
                upgrader_present = self._upgrader is not None and self._upgrader != tid

                can_read = False
                if not writer_active:
                    if already_reader:
                        # Current readers may acquire more reads even if writers are waiting.
                        # But block if a different upgrader is in progress to avoid starvation.
                        can_read = not upgrader_present
                    else:
                        # New readers are blocked if writers are waiting or an upgrader exists.
                        can_read = (not writers_waiting) and (
                            self._upgrader is None)

                if can_read:
                    self._readers[tid] = self._readers.get(tid, 0) + 1
                    return

                if deadline is not None:
                    remaining = deadline - self._now()
                    if remaining <= 0:
                        raise RuntimeError("Timeout while acquiring read lock")
                    self._cond.wait(remaining)
                else:
                    self._cond.wait()

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
            # Re-entrant write
            if self._writer == tid:
                self._write_count += 1
                return

            is_reader = self._readers.get(tid, 0) > 0
            # Deadlock prevention: only one upgrading reader allowed
            if is_reader and (self._upgrader is not None) and (self._upgrader != tid):
                raise ValueError(
                    "Another reader is already upgrading to a write lock")

            deadline = None
            if timeout is not None:
                if timeout <= 0:
                    deadline = self._now()
                else:
                    deadline = self._now() + timeout

            self._waiting_writers += 1
            try:
                if is_reader:
                    # mark as upgrader
                    if self._upgrader is None:
                        self._upgrader = tid
                    elif self._upgrader != tid:
                        # Shouldn't happen due to earlier check, but be safe
                        raise ValueError(
                            "Another reader is already upgrading to a write lock")

                    while True:
                        no_active_writer = (self._writer is None)
                        no_other_readers = not self._has_other_readers(tid)
                        if no_active_writer and no_other_readers:
                            # acquire write
                            self._writer = tid
                            self._write_count = 1
                            # upgrade complete
                            self._upgrader = None
                            return

                        if deadline is not None:
                            remaining = deadline - self._now()
                            if remaining <= 0:
                                raise RuntimeError(
                                    "Timeout while upgrading to write lock")
                            self._cond.wait(remaining)
                        else:
                            self._cond.wait()
                else:
                    # pure writer (not a reader)
                    while True:
                        no_active_writer = (self._writer is None)
                        no_readers = (len(self._readers) == 0)
                        if no_active_writer and no_readers:
                            self._writer = tid
                            self._write_count = 1
                            return

                        if deadline is not None:
                            remaining = deadline - self._now()
                            if remaining <= 0:
                                raise RuntimeError(
                                    "Timeout while acquiring write lock")
                            self._cond.wait(remaining)
                        else:
                            self._cond.wait()
            finally:
                # waiting writers count reduced only when successfully acquired, or on exception
                # If we successfully acquired, we'll decrement here? We need to decrement in both success and failure.
                # If we returned successfully earlier, we wouldn't reach here; thus adjust:
                if self._writer != tid:
                    # didn't acquire
                    self._waiting_writers -= 1
                else:
                    # acquired; decrement the waiting counter as well
                    self._waiting_writers -= 1

    def release(self):
        '''Release the currently held lock.
        In case the current thread holds no lock, a ValueError is thrown.'''
        tid = self._tid()
        with self._cond:
            if self._writer == tid and self._write_count > 0:
                self._write_count -= 1
                if self._write_count == 0:
                    self._writer = None
                    # Wake up everyone: writers and readers
                    self._cond.notify_all()
                return

            rc = self._readers.get(tid, 0)
            if rc > 0:
                if rc == 1:
                    del self._readers[tid]
                else:
                    self._readers[tid] = rc - 1
                # If no readers remain, wake waiting writers
                if not self._readers:
                    self._cond.notify_all()
                return

            raise ValueError("Current thread holds no lock to release")
