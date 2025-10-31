from __future__ import annotations

import json
import importlib
from pathlib import Path
from typing import Iterator, TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from typing import Iterable


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        self._root = Path(storage_path).expanduser().resolve()
        self._root.mkdir(parents=True, exist_ok=True)
        # Conservative selection of common, portable fields
        self._field_whitelist = {
            "app_name",
            "user_id",
            "session_id",
            "title",
            "name",
            "created_at",
            "updated_at",
            "metadata",
            "state",
            "config",
            "summary",
            "description",
            "params",
        }

    def _file_path(
        self,
        *,
        app_name: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
        session: "Session | None" = None,
    ) -> Path:
        if session is not None:
            app_name = getattr(session, "app_name", app_name)
            user_id = getattr(session, "user_id", user_id)
            session_id = getattr(session, "session_id", session_id)

        if not app_name or not user_id or not session_id:
            raise ValueError("app_name, user_id, and session_id are required")

        return self._root / app_name / user_id / f"{session_id}.json"

    def read(self, app_name: str, user_id: str, session_id: str) -> "Session | None":
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.exists():
            return None
        try:
            with path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
        except Exception:
            return None

        meta = payload.get("__class__", {})
        data = payload.get("fields", {})
        cls = self._resolve_class(meta)

        if cls is None:
            # Fallback to a simple dynamic object if Session class isn't importable
            try:
                from types import SimpleNamespace  # type: ignore
            except Exception:
                return None
            obj = SimpleNamespace()
            for k, v in data.items():
                setattr(obj, k, v)
            return obj  # type: ignore[return-value]

        # Try common deserialization entry points
        for method in ("from_dict", "from_json", "deserialize"):
            fn = getattr(cls, method, None)
            if callable(fn):
                try:
                    return fn(data)  # type: ignore[return-value]
                except Exception:
                    pass

        # As a generic fallback, create an uninitialized instance and set attributes
        try:
            obj = cls.__new__(cls)  # type: ignore[call-arg]
            for k, v in data.items():
                try:
                    setattr(obj, k, v)
                except Exception:
                    pass
            return obj  # type: ignore[return-value]
        except Exception:
            return None

    def write(self, session: "Session") -> Path:
        '''Write a session to a JSON file.'''
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "__class__": {
                "module": getattr(session.__class__, "__module__", ""),
                "qualname": getattr(session.__class__, "__qualname__", session.__class__.__name__),
            },
            "fields": self._extract_fields(session),
        }
        tmp_path = path.with_suffix(".json.tmp")
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        tmp_path.replace(path)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink(missing_ok=True)
        except Exception:
            # Best-effort deletion
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> "Iterator[Session]":
        base = self._root / app_name / user_id
        if not base.exists():
            return iter(())

        def _iter() -> Iterator["Session"]:
            for p in sorted(base.glob("*.json")):
                try:
                    with p.open("r", encoding="utf-8") as f:
                        payload = json.load(f)
                    meta = payload.get("__class__", {})
                    data = payload.get("fields", {})
                    cls = self._resolve_class(meta)
                    if cls is None:
                        from types import SimpleNamespace  # type: ignore
                        obj = SimpleNamespace()
                        for k, v in data.items():
                            setattr(obj, k, v)
                        yield obj  # type: ignore[misc]
                        continue
                    obj = None
                    for method in ("from_dict", "from_json", "deserialize"):
                        fn = getattr(cls, method, None)
                        if callable(fn):
                            try:
                                obj = fn(data)
                                break
                            except Exception:
                                pass
                    if obj is None:
                        try:
                            obj = cls.__new__(cls)  # type: ignore[call-arg]
                            for k, v in data.items():
                                try:
                                    setattr(obj, k, v)
                                except Exception:
                                    pass
                        except Exception:
                            obj = None
                    if obj is not None:
                        yield obj  # type: ignore[misc]
                except Exception:
                    continue
        return _iter()

    def _resolve_class(self, meta: dict[str, Any]) -> Optional[type]:
        module = meta.get("module")
        qualname = meta.get("qualname")
        if not module or not qualname:
            return None
        try:
            mod = importlib.import_module(module)
            obj: Any = mod
            for part in qualname.split("."):
                obj = getattr(obj, part)
            if isinstance(obj, type):
                return obj
        except Exception:
            return None
        return None

    def _extract_fields(self, session: Any) -> dict[str, Any]:
        # Prefer a to_dict style method if available
        for method in ("to_dict", "as_dict"):
            fn = getattr(session, method, None)
            if callable(fn):
                try:
                    d = fn()
                    if isinstance(d, dict):
                        return self._sanitize_dict(d)
                except Exception:
                    pass
        # Otherwise, take a conservative subset of attributes
        result: dict[str, Any] = {}
        for key in sorted(self._field_whitelist):
            if hasattr(session, key):
                result[key] = getattr(session, key)
        return self._sanitize_dict(result)

    def _sanitize_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        def convert(v: Any) -> Any:
            if v is None:
                return None
            if isinstance(v, (str, int, float, bool)):
                return v
            if isinstance(v, (list, tuple)):
                return [convert(x) for x in v]
            if isinstance(v, dict):
                return {str(convert(k)): convert(v2) for k, v2 in v.items()}
            # datetime-like
            iso = getattr(v, "isoformat", None)
            if callable(iso):
                try:
                    return v.isoformat()
                except Exception:
                    pass
            # Path-like
            if hasattr(v, "__fspath__"):
                try:
                    return str(Path(v))
                except Exception:
                    pass
            # Fallback to string if not JSON serializable
            try:
                json.dumps(v)
                return v
            except Exception:
                return str(v)
        return {k: convert(v) for k, v in data.items()}
