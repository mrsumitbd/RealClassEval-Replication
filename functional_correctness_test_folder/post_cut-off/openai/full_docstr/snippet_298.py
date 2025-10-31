
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker


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


class SessionManager(SessionManagerPort):
    """Concrete implementation of SessionManagerPort using SQLAlchemy.

    Parameters
    ----------
    engine : Engine
        SQLAlchemy engine to bind the sessionmaker to.
    """

    def __init__(self, engine: Engine) -> None:
        self._session_factory: scoped_session = scoped_session(
            sessionmaker(bind=engine)
        )

    def get_session(self) -> Session:
        """Return a new or existing scoped session.

        Returns
        -------
        Session
            A SQLAlchemy session instance.
        """
        return self._session_factory()

    def remove_session(self) -> None:
        """Remove the current session from the scoped registry."""
        self._session_factory.remove()
