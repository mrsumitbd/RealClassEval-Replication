
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


class SessionManager(SessionManagerPort):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get_session(self) -> Session:
        return self.session

    def remove_session(self) -> None:
        self.session.close()


class ThreadSafeSessionManager(SessionManagerPort):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.Session()

    def remove_session(self, session: Session) -> None:
        session.close()


# Example usage
if __name__ == "__main__":
    database_url = "sqlite:///example.db"
    session_manager = SessionManager(database_url)
    session = session_manager.get_session()
    # Use the session
    session_manager.remove_session()

    thread_safe_session_manager = ThreadSafeSessionManager(database_url)
    thread_safe_session = thread_safe_session_manager.get_session()
    # Use the thread_safe_session
    thread_safe_session_manager.remove_session(thread_safe_session)
