from functools import wraps

class PostgresDatabaseLock:

    def __init__(self, lock_name, timeout=10, db=None):
        self.lock_name = lock_name
        self.timeout = int(timeout)
        self.db = db if db else DB

    def lock(self):
        cursor = self.db.execute_sql('SELECT pg_try_advisory_lock(%s)', self.timeout)
        ret = cursor.fetchone()
        if ret[0] == 0:
            raise Exception(f'acquire postgres lock {self.lock_name} timeout')
        elif ret[0] == 1:
            return True
        else:
            raise Exception(f'failed to acquire lock {self.lock_name}')

    def unlock(self):
        cursor = self.db.execute_sql('SELECT pg_advisory_unlock(%s)', self.timeout)
        ret = cursor.fetchone()
        if ret[0] == 0:
            raise Exception(f'postgres lock {self.lock_name} was not established by this thread')
        elif ret[0] == 1:
            return True
        else:
            raise Exception(f'postgres lock {self.lock_name} does not exist')

    def __enter__(self):
        if isinstance(self.db, PostgresDatabaseLock):
            self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.db, PostgresDatabaseLock):
            self.unlock()

    def __call__(self, func):

        @wraps(func)
        def magic(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return magic