
import json
from pathlib import Path
from typing import Iterator, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .session import Session


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        if session is not None:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        return self.storage_path / f"{app_name}_{user_id}_{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            data = json.load(f)
        from .session import Session
        return Session(
            app_name=data['app_name'],
            user_id=data['user_id'],
            session_id=data['session_id'],
            data=data.get('data', {})
        )

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        data = {
            'app_name': session.app_name,
            'user_id': session.user_id,
            'session_id': session.session_id,
            'data': session.data
        }
        with open(file_path, 'w') as f:
            json.dump(data, f)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        pattern = f"{app_name}_{user_id}_*.json"
        for file_path in self.storage_path.glob(pattern):
            session_id = file_path.stem.split('_')[-1]
            session = self.read(app_name, user_id, session_id)
            if session is not None:
                yield session
