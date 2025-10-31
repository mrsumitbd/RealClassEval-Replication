from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence, Set
from types import SimpleNamespace
from datetime import datetime, date


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = Path(storage_path)

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
            app_name = app_name or getattr(session, "app_name", None)
            user_id = user_id or getattr(session, "user_id", None)
            session_id = session_id or getattr(session, "session_id", None)

        if not app_name or not user_id or not session_id:
            raise ValueError(
                "app_name, user_id, and session_id are required to construct the file path")

        def _safe(s: str) -> str:
            # Simple filesystem-safe sanitizer
            return "".join(c for c in str(s) if c not in r'\/:*?"<>|').strip() or "_"

        return self.storage_path / _safe(app_name) / _safe(user_id) / f"{_safe(session_id)}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

        payload = data.get("payload") if isinstance(data, dict) else None
        meta = data.get("__meta__", {}) if isinstance(data, dict) else {}

        if not isinstance(payload, dict):
            payload = {}

        # Ensure essential fields
        payload.setdefault("app_name", meta.get("app_name", app_name))
        payload.setdefault("user_id", meta.get("user_id", user_id))
        payload.setdefault("session_id", meta.get("session_id", session_id))

        return SimpleNamespace(**payload)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        path = self._file_path(session=session)

        path.parent.mkdir(parents=True, exist_ok=True)

        payload = self._to_jsonable(session)
        meta = {
            "app_name": getattr(session, "app_name", None),
            "user_id": getattr(session, "user_id", None),
            "session_id": getattr(session, "session_id", None),
        }

        data = {
            "__meta__": meta,
            "payload": payload,
            "_format": "adk.session.v1",
        }

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)

        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink(missing_ok=True)
        except TypeError:
            # For Python <3.8 compatibility if needed
            if path.exists():
                path.unlink()

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        base = self.storage_path / app_name / user_id
        if not base.exists() or not base.is_dir():
            return iter(())

        def _iter() -> Iterator['Session']:
            for p in sorted(base.glob("*.json")):
                try:
                    with p.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                    payload = data.get("payload", {})
                    meta = data.get("__meta__", {})
                    if not isinstance(payload, dict):
                        payload = {}
                    payload.setdefault(
                        "app_name", meta.get("app_name", app_name))
                    payload.setdefault("user_id", meta.get("user_id", user_id))
                    if "session_id" not in payload:
                        payload["session_id"] = p.stem
                    yield SimpleNamespace(**payload)
                except Exception:
                    continue

        return _iter()

    def _to_jsonable(self, obj: Any, _seen: Set[int] | None = None) -> Any:
        if _seen is None:
            _seen = set()

        oid = id(obj)
        if oid in _seen:
            return "<recursion>"

        # Primitive types
        if obj is None or isinstance(obj, (bool, int, float, str)):
            return obj

        # Dates and datetimes
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        # Mappings
        if isinstance(obj, Mapping):
            _seen.add(oid)
            return {str(self._to_jsonable(k, _seen)): self._to_jsonable(v, _seen) for k, v in obj.items()}

        # Sequences (but not strings which handled above)
        if isinstance(obj, Sequence):
            _seen.add(oid)
            return [self._to_jsonable(v, _seen) for v in obj]

        # Objects with __dict__
        if hasattr(obj, "__dict__"):
            _seen.add(oid)
            # Filter out callables and private attributes
            d = {k: v for k, v in vars(obj).items(
            ) if not k.startswith("_") and not callable(v)}
            # Ensure essential keys present if available as attributes
            for key in ("app_name", "user_id", "session_id"):
                if hasattr(obj, key):
                    d.setdefault(key, getattr(obj, key))
            return {k: self._to_jsonable(v, _seen) for k, v in d.items()}

        # Fallback to string representation
        try:
            return str(obj)
        except Exception:
            return "<unserializable>"
