
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.engine import Engine


class SessionManagerPort(ABC):
    """Interface for SQLAlchemy session management operations.

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
    """Concrete implementation of :class:`SessionManagerPort` using
    SQLAlchemy's :class:`scoped_session` for thread‑local session handling.
    """

    def __init__(self, engine: Engine, **session_kwargs) -> None:
        """
        Parameters
        ----------
        engine : Engine
            SQLAlchemy engine to bind the sessionmaker to.
        session_kwargs : dict
            Optional keyword arguments forwarded to :class:`sessionmaker`.
            Common options include ``autocommit``, ``autoflush``, and
            ``expire_on_commit``.
        """
        self._session_factory = sessionmaker(bind=engine, **session_kwargs)
        self._scoped_session = scoped_session(self._session_factory)

    def get_session(self) -> Session:
        """Return a thread‑local SQLAlchemy session.

        The session is created lazily on first access and cached for the
        duration of the current thread or context.
        """
        return self._scoped_session()

    def remove_session(self) -> None:
        """Remove the current thread‑local session.

        This should be called when the session is no longer needed, e.g.
        at the end of a request or a unit of work, to avoid leaking
        connections.
        """
        self._scoped_session.remove()
