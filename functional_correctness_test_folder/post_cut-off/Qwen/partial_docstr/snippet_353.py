
from pathlib import Path
import json
from typing import Iterator, Optional


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
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> Optional['Session']:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            with file_path.open('r') as f:
                data = json.load(f)
                return Session(**data)
        return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as f:
            json.dump(session.to_dict(), f)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator['Session']:
        session_dir = self.storage_path / app_name / user_id
        if session_dir.exists() and session_dir.is_dir():
            for file_path in session_dir.glob('*.json'):
                with file_path.open('r') as f:
                    data = json.load(f)
                    yield Session(**data)


class Session:
    def __init__(self, app_name: str, user_id: str, session_id: str, data: dict):
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.data = data

    def to_dict(self) -> dict:
        return {
            'app_name': self.app_name,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'data': self.data
        }
