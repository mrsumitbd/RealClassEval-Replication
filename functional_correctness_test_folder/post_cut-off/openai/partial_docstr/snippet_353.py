
import json
from pathlib import Path
from typing import Iterator, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .session import Session  # Adjust import path as needed


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: 'Session | None' = None,
    ) -> Path:
        if session is not None:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "app_name, user_id and session_id must be provided")
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Assume Session can be instantiated from the JSON dict
            from .session import Session  # Lazy import to avoid circular dependency
            return Session(**data)
        except Exception:
            return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Serialize only serializable fields; use session.__dict__ as a simple approach
        data = {k: v for k, v in session.__dict__.items() if isinstance(
            v, (str, int, float, bool, list, dict))}
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if path.is_file():
            path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator['Session']:
        base_dir = self.storage_path / app_name / user_id
        if not base_dir.is_dir():
            return iter([])
        for file_path in base_dir.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                from .session import Session  # Lazy import
                yield Session(**data)
            except Exception:
                continue
