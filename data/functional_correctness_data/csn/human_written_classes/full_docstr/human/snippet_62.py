from threading import Condition, Lock, current_thread
from time import time

class ReadWriteLock:
    """Read-Write lock class. A read-write lock differs from a standard
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
    """

    def __init__(self):
        """Initialize this read-write lock."""
        self.__condition = Condition(Lock())
        self.__writer = None
        self.__upgradewritercount = 0
        self.__pendingwriters = []
        self.__readers = {}

    def acquire_read(self, *, timeout=None):
        """Acquire a read lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.

        In case timeout is None, the call to acquire_read blocks until the
        lock request can be serviced.

        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown."""
        if timeout is not None:
            endtime = time() + timeout
        me = current_thread()
        self.__condition.acquire()
        try:
            if self.__writer is me:
                self.__writercount += 1
                return
            while True:
                if self.__writer is None:
                    if self.__upgradewritercount or self.__pendingwriters:
                        if me in self.__readers:
                            self.__readers[me] += 1
                            return
                    else:
                        self.__readers[me] = self.__readers.get(me, 0) + 1
                        return
                if timeout is not None:
                    remaining = endtime - time()
                    if remaining <= 0:
                        raise RuntimeError('Acquiring read lock timed out')
                    self.__condition.wait(remaining)
                else:
                    self.__condition.wait()
        finally:
            self.__condition.release()

    def acquire_write(self, *, timeout=None):
        """Acquire a write lock for the current thread, waiting at most
        timeout seconds or doing a non-blocking check in case timeout is <= 0.

        In case the write lock cannot be serviced due to the deadlock
        condition mentioned above, a ValueError is raised.

        In case timeout is None, the call to acquire_write blocks until the
        lock request can be serviced.

        In case the timeout expires before the lock could be serviced, a
        RuntimeError is thrown."""
        if timeout is not None:
            endtime = time() + timeout
        me, upgradewriter = (current_thread(), False)
        self.__condition.acquire()
        try:
            if self.__writer is me:
                self.__writercount += 1
                return
            elif me in self.__readers:
                if self.__upgradewritercount:
                    raise ValueError('Inevitable dead lock, denying write lock')
                upgradewriter = True
                self.__upgradewritercount = self.__readers.pop(me)
            else:
                self.__pendingwriters.append(me)
            while True:
                if not self.__readers and self.__writer is None:
                    if self.__upgradewritercount:
                        if upgradewriter:
                            self.__writer = me
                            self.__writercount = self.__upgradewritercount + 1
                            self.__upgradewritercount = 0
                            return
                    elif self.__pendingwriters[0] is me:
                        self.__writer = me
                        self.__writercount = 1
                        self.__pendingwriters = self.__pendingwriters[1:]
                        return
                if timeout is not None:
                    remaining = endtime - time()
                    if remaining <= 0:
                        if upgradewriter:
                            self.__readers[me] = self.__upgradewritercount
                            self.__upgradewritercount = 0
                        else:
                            self.__pendingwriters.remove(me)
                        raise RuntimeError('Acquiring write lock timed out')
                    self.__condition.wait(remaining)
                else:
                    self.__condition.wait()
        finally:
            self.__condition.release()

    def release(self):
        """Release the currently held lock.

        In case the current thread holds no lock, a ValueError is thrown."""
        me = current_thread()
        self.__condition.acquire()
        try:
            if self.__writer is me:
                self.__writercount -= 1
                if not self.__writercount:
                    self.__writer = None
                    self.__condition.notify_all()
            elif me in self.__readers:
                self.__readers[me] -= 1
                if not self.__readers[me]:
                    del self.__readers[me]
                    if not self.__readers:
                        self.__condition.notify_all()
            else:
                raise ValueError('Trying to release unheld lock')
        finally:
            self.__condition.release()