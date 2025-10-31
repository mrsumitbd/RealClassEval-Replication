from sqlalchemy.orm.session import Session, sessionmaker

class SessionHolder:

    def __init__(self, sess_cls):
        self._sess_cls = sess_cls

    def __call__(self) -> Session:
        return self._sess_cls()