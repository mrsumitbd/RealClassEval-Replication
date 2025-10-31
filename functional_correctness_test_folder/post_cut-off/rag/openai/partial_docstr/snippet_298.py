
from abc import ABC, abstractmethod
from typing import Callable, Optional

from sqlalchemy.orm import Session, sessionmaker, scoped_session


class SessionManagerPort(ABC):
    """Interface for SQLAlchemy session management operations.

    This interface defines the contract for session management adapters,
    providing methods for retrieving and managing database sessions
    in a synchronous context.
    Implementing classes must provide mechanisms to:
    1. Retrieve a properly configured SQLAlchemy session
    2. Release/remove sessions when they're no longer needed
    """

    @abstractmethod
    def get_session(self) -> Session:
        """Retrieve a SQLAlchemy session.

        Returns:
            Session: A SQLAlchemy session object
        """
        pass

    @abstractmethod
    def remove_session(self) -> None:
        """Remove the current session from the registry."""
        pass


class SQLAlchemySessionManager(SessionManagerPort):
    """Concrete implementation of SessionManagerPort using SQLAlchemy.

    Parameters
    ----------
    session_factory : Callable[[], Session]
        A callable that returns a new SQLAlchemy Session instance.
        Typically this is a `sessionmaker` or a `scoped_session`.
    """

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        if not callable(session_factory):
            raise TypeError("session_factory must be callable")
        self._session_factory = session_factory
        self._session: Optional[Session] = None

    def get_session(self) -> Session:
        """Return a session, creating it if necessary."""
        if self._session is None:
            self._session = self._session_factory()
        return self._session

    def remove_session(self) -> None:
        """Close and discard the current session."""
        if self._session is not None:
            try:
                self._session.close()
            finally:
                self._session = None


# Example usage
if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import declarative_base, Session

    engine = create_engine("sqlite:///:memory:", echo=False)
    Base = declarative_base()

    # Create a sessionmaker bound to the engine
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    # Instantiate the manager
    manager = SQLAlchemySessionManager(SessionLocal)

    # Retrieve a session
    session = manager.get_session()
    print(f"Session type: {type(session)}")

    # Clean up
    manager.remove_session()
