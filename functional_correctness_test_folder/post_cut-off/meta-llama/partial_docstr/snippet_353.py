
import json
from pathlib import Path
from typing import Iterator, Optional


class Session:
    # Assuming Session class is defined elsewhere
    pass


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    def _file_path(self, *, app_name: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None, session: Optional['Session'] = None) -> Path:
        if session:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "Either session or all of app_name, user_id, and session_id must be provided")
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> Optional['Session']:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Assuming Session class has a from_dict method
                return Session.from_dict(data)
        except FileNotFoundError:
            return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            # Assuming Session class has a to_dict method
            json.dump(session.to_dict(), file)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            file_path.unlink()
        except FileNotFoundError:
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator['Session']:
        user_dir = self.storage_path / app_name / user_id
        if user_dir.exists():
            for file in user_dir.glob("*.json"):
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                        # Assuming Session class has a from_dict method
                        yield Session.from_dict(data)
                except json.JSONDecodeError:
                    # Handle JSON decode error
                    pass
