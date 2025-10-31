class DBMContext:
    """
    A context manager to access the key-value store in a concurrent-safe manner.
    """
    __slots__ = ('filename', 'mode', 'readonly', 'lockfile', 'db')

    def __init__(self, filename, mode, readonly):
        self.filename = filename
        self.mode = mode
        self.readonly = readonly
        self.lockfile = open(filename + '.lock', 'w+b')

    def __enter__(self):
        lock(self.lockfile, self.readonly)
        self.db = dbm.open(self.filename, 'c', self.mode)
        return self.db

    def __exit__(self, exval, extype, tb):
        self.db.close()
        unlock(self.lockfile)
        self.lockfile.close()