from pathlib import Path
import json
from typing import Iterator, Optional


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: 'Session | None' = None
    ) -> Path:
        '''Construct the JSON file path for a session.'''
        if session is not None:
            app_name = getattr(session, "app_name", None)
            user_id = getattr(session, "user_id", None)
            session_id = getattr(session, "session_id", None)
        if not (app_name and user_id and session_id):
            raise ValueError(
                "app_name, user_id, and session_id must be provided")
        dir_path = self.storage_path / app_name / user_id
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        from adk.session import Session  # type: ignore
        return Session.from_json(data)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        file_path = self._file_path(session=session)
        # Only serialize a subset of fields
        data = session.to_json()
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return file_path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        file_path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if file_path.exists():
            file_path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        dir_path = self.storage_path / app_name / user_id
        if not dir_path.exists() or not dir_path.is_dir():
            return
        from adk.session import Session  # type: ignore
        for file in dir_path.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            yield Session.from_json(data)
