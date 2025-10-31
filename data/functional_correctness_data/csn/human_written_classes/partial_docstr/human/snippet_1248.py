from sqlalchemy.orm import scoped_session
from trailblazer.store.database import get_session, initialize_database

class DatabaseResource:
    """
    Setup the database and ensure resources are released when the
    CLI command has been processed.
    """

    def __init__(self, db_uri: str):
        self.db_uri = db_uri

    def __enter__(self):
        initialize_database(self.db_uri)

    def __exit__(self, _, __, ___):
        session: scoped_session = get_session()
        session.remove()