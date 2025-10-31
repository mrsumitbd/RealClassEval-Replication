
from abc import ABC, abstractmethod
from typing import Optional

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
    engine
        SQLAlchemy Engine instance to bind the sessionmaker to.
    session_factory
        Optional custom sessionmaker factory. If not provided, a default
        sessionmaker bound to the engine will be used.
    """

    def __init__(self, engine, session_factory: Optional[sessionmaker] = None):
        if session_factory is None:
            session_factory = sessionmaker(bind=engine)
        # Use scoped_session to ensure thread‑local sessions
        self._scoped_session = scoped_session(session_factory)

    def get_session(self) -> Session:
        """Return a thread‑local SQLAlchemy session."""
        return self._scoped_session()

    def remove_session(self) -> None:
        """Remove the current thread‑local session."""
        self._scoped_session.remove()
