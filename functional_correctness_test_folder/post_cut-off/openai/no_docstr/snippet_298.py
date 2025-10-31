
from abc import ABC
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class SessionManagerPort(ABC):
    """
    Concrete implementation of a session manager that provides SQLAlchemy
    sessions backed by a database engine.
    """

    def __init__(self, connection_string: str):
        """
        Initialize the session manager with a database connection string.

        Args:
            connection_string: A database URL, e.g. 'sqlite:///example.db'
        """
        self._engine = create_engine(
            connection_string, echo=False, future=True)
        self._SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine, future=True
        )
        self._session: Optional[Session] = None

    def get_session(self) -> Session:
        """
        Retrieve a SQLAlchemy session. If a session has already been created
        for the current instance, it will be returned; otherwise a new session
        will be created.

        Returns:
            Session: A SQLAlchemy session object
        """
        if self._session is None or not self._session.is_active:
            self._session = self._SessionLocal()
        return self._session

    def remove_session(self) -> None:
        """
        Close the current session and release any resources. After calling
        this method, subsequent calls to `get_session` will create a new
        session.
        """
        if self._session is not None:
            self._session.close()
            self._session = None
