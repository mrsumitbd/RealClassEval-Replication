
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine


class SessionManagerPort(ABC):

    @abstractmethod
    def get_session(self) -> Session:
        '''Retrieve a SQLAlchemy session.
        This method provides a database session that can be used for
        querying, creating, updating, and deleting data.
        Returns:
            Session: A SQLAlchemy session object
        Examples:
            >>> session = session_manager.get_session()
            >>> results = session.query(User).all()
        '''
        pass

    @abstractmethod
    def remove_session(self) -> None:
        pass


class SQLAlchemySessionManager(SessionManagerPort):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def remove_session(self) -> None:
        session = self.SessionLocal()
        session.close()
