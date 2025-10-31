
import json
from pathlib import Path
from typing import Iterator, Optional


class Session:
    # Assuming Session class is defined elsewhere
    def __init__(self, app_name: str, user_id: str, session_id: str, data: dict):
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.data = data


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        '''Construct the JSON file path for a session.'''
        if session:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id

        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "Either session or all of app_name, user_id, and session_id must be provided")

        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return Session(app_name, user_id, session_id, data)
        except FileNotFoundError:
            return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(session.data, file)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            file_path.unlink()
        except FileNotFoundError:
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        user_path = self.storage_path / app_name / user_id
        if user_path.exists():
            for file_path in user_path.glob("*.json"):
                session_id = file_path.stem
                yield self.read(app_name, user_id, session_id)


# Example usage
if __name__ == "__main__":
    storage_path = Path("sessions")
    serializer = JSONSessionSerializer(storage_path)

    session = Session("app1", "user1", "session1", {"key": "value"})
    file_path = serializer.write(session)
    print(f"Session written to {file_path}")

    loaded_session = serializer.read("app1", "user1", "session1")
    print(f"Loaded session: {loaded_session.data}")

    for saved_session in serializer.list_saved(app_name="app1", user_id="user1"):
        print(f"Saved session: {saved_session.session_id}")

    serializer.delete("app1", "user1", "session1")
