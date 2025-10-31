
import json
import os
from pathlib import Path
from typing import Iterator, Optional, Any

# NOTE: In a real implementation the `Session` type would be imported from the
# ADK library.  For the purposes of this serializer we treat a session as a
# simple mapping of the fields that are persisted.
Session = Any


class JSONSessionSerializer:
    """Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    """

    def __init__(self, storage_path: Path) -> None:
        """Initialize a new instance of JSONSessionSerializer."""
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: "Session | None" = None,
    ) -> Path:
        """Construct the JSON file path for a session."""
        if session is not None:
            app_name = getattr(session, "app_name", app_name)
            user_id = getattr(session, "user_id", user_id)
            session_id = getattr(session, "session_id", session_id)

        if not all([app_name, user_id, session_id]):
            raise ValueError(
                "app_name, user_id and session_id must be provided")

        return (
            self.storage_path
            / app_name
            / user_id
            / f"{session_id}.json"
        )

    def read(self, app_name: str, user_id: str, session_id: str) -> "Session | None":
        """Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        """
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.is_file():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # In a real implementation we would construct a Session instance.
            # Here we simply return the raw data dictionary.
            return data
        except Exception:
            return None

    def write(self, session: "Session") -> Path:
        """Write a session to a JSON file."""
        # Extract the subset of fields we want to persist.
        payload = {
            "app_name": getattr(session, "app_name"),
            "user_id": getattr(session, "user_id"),
            "session_id": getattr(session, "session_id"),
            # Persist any additional data that the session might expose.
            # We use a simple introspection approach.
            "data": getattr(session, "data", {}),
        }
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, sort_keys=True)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        """Delete a session's JSON file."""
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> Iterator["Session"]:
        """List saved sessions."""
        base_dir = self.storage_path / app_name / user_id
        if not base_dir.is_dir():
            return iter([])
        for file_path in base_dir.glob("*.json"):
            try:
                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                yield data
            except Exception:
                # Skip files that cannot be read
                continue
