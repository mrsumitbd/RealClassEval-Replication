
import json
from pathlib import Path
from typing import Iterator, Optional


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path

    def _file_path(self, *, app_name: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None, session: 'Optional[Session]' = None) -> Path:
        '''Construct the JSON file path for a session.'''
        if session:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "Either session or all of app_name, user_id, and session_id must be provided")
        return self.storage_path / f'{app_name}_{user_id}_{session_id}.json'

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Optional[Session]':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return Session(**data)
        except FileNotFoundError:
            return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(session.to_dict(), f)
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
        pattern = f'{app_name}_{user_id}_*.json'
        for file_path in self.storage_path.glob(pattern):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    yield Session(**data)
            except json.JSONDecodeError:
                continue
