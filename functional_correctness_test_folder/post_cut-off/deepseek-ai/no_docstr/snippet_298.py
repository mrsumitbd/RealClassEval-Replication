
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


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
        '''Remove the current SQLAlchemy session.
        This method ensures that the session is properly closed and removed,
        preventing any potential memory leaks or connection issues.
        Examples:
            >>> session_manager.remove_session()
        '''
        pass
