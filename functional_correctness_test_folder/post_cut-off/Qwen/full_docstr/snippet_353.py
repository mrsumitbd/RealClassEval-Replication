
from pathlib import Path
import json
from typing import Iterator, Optional


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

    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        return cls(
            app_name=data['app_name'],
            user_id=data['user_id'],
            session_id=data['session_id'],
            data=data['data']
        )


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path

    def _file_path(self, *, app_name: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None, session: Optional[Session] = None) -> Path:
        '''Construct the JSON file path for a session.'''
        if session:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> Optional[Session]:
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            with file_path.open('r') as file:
                data = json.load(file)
                return Session.from_dict(data)
        return None

    def write(self, session: Session) -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            json.dump(session.to_dict(), file, indent=4)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator[Session]:
        '''List saved sessions.'''
        dir_path = self.storage_path / app_name / user_id
        if dir_path.exists() and dir_path.is_dir():
            for file_path in dir_path.glob('*.json'):
                with file_path.open('r') as file:
                    data = json.load(file)
                    yield Session.from_dict(data)
