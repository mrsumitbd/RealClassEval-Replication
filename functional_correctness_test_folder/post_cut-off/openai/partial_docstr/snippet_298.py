
from abc import ABC, abstractmethod
from typing import Optional
import threading

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine


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

        This method provides a database session that can be used for
        querying, creating, updating, and deleting data.

        Returns:
            Session: A SQLAlchemy session object

        Examples:
            >>> session = session_manager.get_session()
            >>> results = session.query(User).all()
        """
        pass

    @abstractmethod
    def remove_session(self) -> None:
        """Remove the current session from the registry.

        This method should be called to clean up the session when it's
        no longer needed, helping to prevent resource leaks and ensure
        proper session management.
        """
        pass


class SQLAlchemySessionManager(SessionManagerPort):
    """Concrete implementation of SessionManagerPort using SQLAlchemy.

    Parameters
    ----------
    engine : Engine
        SQLAlchemy engine to bind the sessionmaker to.
    session_factory : Optional[sessionmaker]
        Optional custom sessionmaker. If not provided, a default
        sessionmaker bound to the given engine will be used.
    """

    def __init__(self, engine: Engine, session_factory: Optional[sessionmaker] = None):
        self._engine = engine
        self._session_factory = session_factory or sessionmaker(
            bind=self._engine)
        # Thread‑local storage to keep a session per thread
        self._thread_local = threading.local()

    def get_session(self) -> Session:
        """Return a thread‑local SQLAlchemy session.

        If a session does not exist for the current thread, a new one
        is created and stored in thread‑local storage.
        """
        if not hasattr(self._thread_local, "session"):
            self._thread_local.session = self._session_factory()
        return self._thread_local.session

    def remove_session(self) -> None:
        """Close and remove the thread‑local session.

        This method should be called when the session is no longer needed
        to free resources and avoid leaks.
        """
        session: Optional[Session] = getattr(
            self._thread_local, "session", None)
        if session is not None:
            session.close()
            del self._thread_local.session
