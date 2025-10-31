
import json
import os
from pathlib import Path
from typing import Iterator, Optional, Any, Dict

# The real Session type is expected to be provided by the ADK library.
# For the purposes of this serializer we treat it as a generic object
# that exposes the attributes used below.
Session = Any


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: 'Session | None' = None,
    ) -> Path:
        '''Construct the JSON file path for a session.'''
        if session is not None:
            app_name = getattr(session, "app_name", None)
            user_id = getattr(session, "user_id", None)
            session_id = getattr(session, "session_id", None)

        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "app_name, user_id and session_id must be provided")

        return (
            self.storage_path
            / app_name
            / user_id
            / f"{session_id}.json"
        )

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        # Construct a simple Session-like object.  The real ADK Session
        # may have a more complex constructor; here we just create a
        # lightweight object with the expected attributes.
        class _Session:
            def __init__(self, **kwargs: Any) -> None:
                for k, v in kwargs.items():
                    setattr(self, k, v)

        return _Session(**data)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        # Extract only the fields we care about
        payload: Dict[str, Any] = {
            "app_name": getattr(session, "app_name", None),
            "user_id": getattr(session, "user_id", None),
            "session_id": getattr(session, "session_id", None),
            "created_at": getattr(session, "created_at", None),
            "data": getattr(session, "data", None),
        }

        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, default=str)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if path.exists():
            path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator['Session']:
        '''List saved sessions.'''
        base_dir = self.storage_path / app_name / user_id
        if not base_dir.exists():
            return iter([])

        for file_path in base_dir.glob("*.json"):
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Reuse the same lightweight Session class

            class _Session:
                def __init__(self, **kwargs: Any) -> None:
                    for k, v in kwargs.items():
                        setattr(self, k, v)

            yield _Session(**data)
