
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session, scoped_session, sessionmaker
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
        self.session_factory = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self) -> Session:
        return self.session_factory()

    def remove_session(self) -> None:
        self.session_factory.remove()


# Example usage
if __name__ == "__main__":
    database_url = "sqlite:///example.db"
    session_manager = SQLAlchemySessionManager(database_url)
    session = session_manager.get_session()
    try:
        # Use the session
        print(session)
    finally:
        session_manager.remove_session()
