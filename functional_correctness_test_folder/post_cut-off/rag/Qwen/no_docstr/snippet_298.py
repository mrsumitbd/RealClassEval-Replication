
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine


class SessionManagerPort(ABC):
    '''Interface for SQLAlchemy session management operations.
    This interface defines the contract for session management adapters,
    providing methods for retrieving and managing database sessions
    in a synchronous context.
    Implementing classes must provide mechanisms to:
    1. Retrieve a properly configured SQLAlchemy session
    2. Release/remove sessions when they're no longer needed
    '''
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
        '''Remove the current session from the registry.
        This method should be called to clean up the session when it's
        no longer needed, helping to prevent resource leaks and ensure
        proper session management.
        '''
        pass


class SQLAlchemySessionManager(SessionManagerPort):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        '''Retrieve a SQLAlchemy session.
        This method provides a database session that can be used for
        querying, creating, updating, and deleting data.
        Returns:
            Session: A SQLAlchemy session object
        '''
        return self.SessionLocal()

    def remove_session(self) -> None:
        '''Remove the current session from the registry.
        This method should be called to clean up the session when it's
        no longer needed, helping to prevent resource leaks and ensure
        proper session management.
        '''
        self.SessionLocal.remove()
