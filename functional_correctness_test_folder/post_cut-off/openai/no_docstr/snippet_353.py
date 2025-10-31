
import json
from pathlib import Path
from typing import Iterator, Any, Optional


class JSONSessionSerializer:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: "Session | None" = None,
    ) -> Path:
        if session is not None:
            app_name = getattr(session, "app_name", None)
            user_id = getattr(session, "user_id", None)
            session_id = getattr(session, "session_id", None)

        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "app_name, user_id and session_id must be provided")

        return self.storage_path / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> "Session | None":
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Attempt to reconstruct a Session object if possible
            if isinstance(data, dict):
                # If the Session class is a dataclass or has a constructor that accepts **kwargs
                try:
                    return type("Session", (), data)()
                except Exception:
                    return data
            return data
        except Exception:
            return None

    def write(self, session: "Session") -> Path:
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Serialize session: try __dict__, else try dataclasses.asdict
        try:
            data = session.__dict__
        except Exception:
            data = {}
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator["Session"]:
        base_dir = self.storage_path / app_name / user_id
        if not base_dir.is_dir():
            return iter([])
        for file_path in base_dir.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    try:
                        yield type("Session", (), data)()
                    except Exception:
                        yield data
                else:
                    yield data
            except Exception:
                continue
