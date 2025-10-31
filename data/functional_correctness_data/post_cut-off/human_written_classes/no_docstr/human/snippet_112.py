from functools import wraps
from playhouse.pool import PooledMySQLDatabase, PooledPostgresqlDatabase

class MysqlDatabaseLock:

    def __init__(self, lock_name, timeout=10, db=None):
        self.lock_name = lock_name
        self.timeout = int(timeout)
        self.db = db if db else DB

    def lock(self):
        cursor = self.db.execute_sql('SELECT GET_LOCK(%s, %s)', (self.lock_name, self.timeout))
        ret = cursor.fetchone()
        if ret[0] == 0:
            raise Exception(f'acquire mysql lock {self.lock_name} timeout')
        elif ret[0] == 1:
            return True
        else:
            raise Exception(f'failed to acquire lock {self.lock_name}')

    def unlock(self):
        cursor = self.db.execute_sql('SELECT RELEASE_LOCK(%s)', (self.lock_name,))
        ret = cursor.fetchone()
        if ret[0] == 0:
            raise Exception(f'mysql lock {self.lock_name} was not established by this thread')
        elif ret[0] == 1:
            return True
        else:
            raise Exception(f'mysql lock {self.lock_name} does not exist')

    def __enter__(self):
        if isinstance(self.db, PooledMySQLDatabase):
            self.lock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(self.db, PooledMySQLDatabase):
            self.unlock()

    def __call__(self, func):

        @wraps(func)
        def magic(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return magic