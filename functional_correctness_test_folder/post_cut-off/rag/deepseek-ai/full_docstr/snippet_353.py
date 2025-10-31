
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
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        '''Construct the JSON file path for a session.'''
        if session is not None:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
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
            created_at=data['created_at'],
            expires_at=data.get('expires_at'),
            data=data.get('data', {})
        )

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            'app_name': session.app_name,
            'user_id': session.user_id,
            'session_id': session.session_id,
            'created_at': session.created_at,
            'expires_at': session.expires_at,
            'data': session.data
        }

        with open(file_path, 'w') as f:
            json.dump(data, f)

        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        user_dir = self.storage_path / app_name / user_id
        if not user_dir.exists():
            return

        for session_file in user_dir.glob('*.json'):
            session_id = session_file.stem
            session = self.read(app_name, user_id, session_id)
            if session is not None:
                yield session
