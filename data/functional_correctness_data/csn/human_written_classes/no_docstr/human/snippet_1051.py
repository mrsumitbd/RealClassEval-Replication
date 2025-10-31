class EmptyTransactionalHolder:

    def __init__(self):
        self._session = None

    @property
    def session(self):
        return self._session