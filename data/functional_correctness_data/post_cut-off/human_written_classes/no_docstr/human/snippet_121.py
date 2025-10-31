import uuid
from valkey.lock import Lock

class RedisDistributedLock:

    def __init__(self, lock_key, lock_value=None, timeout=10, blocking_timeout=1):
        self.lock_key = lock_key
        if lock_value:
            self.lock_value = lock_value
        else:
            self.lock_value = str(uuid.uuid4())
        self.timeout = timeout
        self.lock = Lock(REDIS_CONN.REDIS, lock_key, timeout=timeout, blocking_timeout=blocking_timeout)

    def acquire(self):
        return self.lock.acquire()

    def release(self):
        return self.lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.release()