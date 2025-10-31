
from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


class SessionManagerPort(ABC):

    @abstractmethod
    def get_session(self) -> Session:
        '''Retrieve a SQLAlchemy session.'''
        pass

    @abstractmethod
    def remove_session(self) -> None:
        pass


class SessionManager(SessionManagerPort):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        self._session = None

    def get_session(self) -> Session:
        if self._session is None:
            self._session = self.SessionLocal()
        return self._session

    def remove_session(self) -> None:
        if self._session is not None:
            self._session.close()
            self._session = None
