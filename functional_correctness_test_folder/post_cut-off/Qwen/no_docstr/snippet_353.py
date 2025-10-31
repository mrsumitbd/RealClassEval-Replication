
import json
from pathlib import Path
from typing import Iterator, Optional


class Session:
    def __init__(self, session_id: str, data: dict):
        self.session_id = session_id
        self.data = data

    def to_dict(self) -> dict:
        return {
            'session_id': self.session_id,
            'data': self.data
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        return cls(session_id=data['session_id'], data=data['data'])


class JSONSessionSerializer:

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(self, *, app_name: Optional[str] = None, user_id: Optional[str] = None, session_id: Optional[str] = None, session: Optional[Session] = None) -> Path:
        if session:
            app_name = session.data.get('app_name')
            user_id = session.data.get('user_id')
            session_id = session.session_id
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> Optional[Session]:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            with file_path.open('r') as file:
                data = json.load(file)
                return Session.from_dict(data)
        return None

    def write(self, session: Session) -> Path:
        file_path = self._file_path(session=session)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            json.dump(session.to_dict(), file)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator[Session]:
        user_dir = self.storage_path / app_name / user_id
        if user_dir.exists() and user_dir.is_dir():
            for file_path in user_dir.glob('*.json'):
                with file_path.open('r') as file:
                    data = json.load(file)
                    yield Session.from_dict(data)
