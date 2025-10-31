
import json
from pathlib import Path
from typing import Iterator, Optional, Union


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    def _file_path(self, *, app_name: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None, session: Optional['Session'] = None) -> Path:
        if session is not None:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> Optional['Session']:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            data = json.load(f)
        from adk.session import Session
        return Session(**data)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(session.to_dict(), f)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator['Session']:
        user_path = self.storage_path / app_name / user_id
        if not user_path.exists():
            return iter(())
        from adk.session import Session
        return (Session(**json.loads(f.read_text())) for f in user_path.glob('*.json'))
