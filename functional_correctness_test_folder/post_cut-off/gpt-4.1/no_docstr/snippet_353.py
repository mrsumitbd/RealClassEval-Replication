
from pathlib import Path
from typing import Iterator, Optional
import json


class Session:
    def __init__(self, app_name: str, user_id: str, session_id: str, data: dict):
        self.app_name = app_name
        self.user_id = user_id
        self.session_id = session_id
        self.data = data

    def to_dict(self):
        return {
            "app_name": self.app_name,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            app_name=d["app_name"],
            user_id=d["user_id"],
            session_id=d["session_id"],
            data=d["data"]
        )


class JSONSessionSerializer:

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        if session is not None:
            app_name = session.app_name
            user_id = session.user_id
            session_id = session.session_id
        if not (app_name and user_id and session_id):
            raise ValueError(
                "app_name, user_id, and session_id must be provided")
        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return Session.from_dict(data)

    def write(self, session: 'Session') -> Path:
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if path.exists():
            path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        dir_path = self.storage_path / app_name / user_id
        if not dir_path.exists() or not dir_path.is_dir():
            return
        for file in dir_path.glob("*.json"):
            with file.open("r", encoding="utf-8") as f:
                data = json.load(f)
            yield Session.from_dict(data)
