class _Transactor:

    def __init__(self, store, callable):
        self.store = store
        self.callable = callable

    def __call__(self, box):
        return self.store.transact(self.callable, box)

    def __repr__(self):
        return '<Transaction in: %s of: %s>' % (self.store, self.callable)