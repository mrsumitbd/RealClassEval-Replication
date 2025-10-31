from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Iterator, Any


class JSONSessionSerializer:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = Path(storage_path)

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
            raise ValueError(
                "app_name, user_id and session_id must be provided")

        return self.storage_path / app_name / user_id / f"{session_id}.json"

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

        meta = payload.get("__meta__", {})
        cls_module = meta.get("class_module")
        cls_name = meta.get("class_name")

        data = payload.get("data", payload)

        # Attempt to rehydrate using stored class metadata
        if cls_module and cls_name:
            try:
                module = importlib.import_module(cls_module)
                cls = getattr(module, cls_name)
                inst = self._construct_session(cls, data)
                if inst is not None:
                    return inst
            except Exception:
                pass

        # Fallback heuristics: try to import a symbol named "Session" if available
        try:
            cls = self._import_default_session_class()
            inst = self._construct_session(cls, data)
            if inst is not None:
                return inst
        except Exception:
            pass

        return None

    def write(self, session: "Session") -> Path:
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = self._serialize_session(session)
        payload = {
            "__meta__": {
                "class_module": session.__class__.__module__,
                "class_name": session.__class__.__name__,
            },
            "data": data,
        }

        # Atomic write
        path_parent_str = str(path.parent)
        with NamedTemporaryFile("w", delete=False, dir=path_parent_str, encoding="utf-8") as tmp:
            tmp_path = Path(tmp.name)
            json.dump(payload, tmp, ensure_ascii=False,
                      indent=2, sort_keys=True)
        os.replace(tmp_path, path)

        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink()
        except FileNotFoundError:
            return

    def list_saved(self, *, app_name: str, user_id: str) -> "Iterator[Session]":
        base = self.storage_path / app_name / user_id
        if not base.exists():
            return iter(())

        def _iter() -> Iterator["Session"]:
            for p in sorted(base.glob("*.json")):
                try:
                    with p.open("r", encoding="utf-8") as f:
                        payload = json.load(f)
                    meta = payload.get("__meta__", {})
                    data = payload.get("data", payload)
                    cls = None
                    if "class_module" in meta and "class_name" in meta:
                        try:
                            module = importlib.import_module(
                                meta["class_module"])
                            cls = getattr(module, meta["class_name"])
                        except Exception:
                            cls = None
                    if cls is None:
                        try:
                            cls = self._import_default_session_class()
                        except Exception:
                            cls = None
                    if cls is not None:
                        inst = self._construct_session(cls, data)
                        if inst is not None:
                            yield inst
                except Exception:
                    continue
        return _iter()

    def _serialize_session(self, session: Any) -> dict:
        # Try common serialization hooks
        for attr in ("to_dict", "dict", "model_dump"):
            fn = getattr(session, attr, None)
            if callable(fn):
                try:
                    data = fn()
                    if isinstance(data, dict):
                        return data
                except Exception:
                    pass
        # Fallback to __dict__
        if hasattr(session, "__dict__"):
            return dict(session.__dict__)
        # Last resort: try dataclasses.asdict without importing unless needed
        try:
            from dataclasses import asdict, is_dataclass
            if is_dataclass(session):
                return asdict(session)
        except Exception:
            pass
        raise TypeError("Unable to serialize session object to dict")

    def _construct_session(self, cls: Any, data: dict) -> Any | None:
        # Try common construction patterns
        for name in ("from_dict", "from_json", "model_validate", "parse_obj"):
            fn = getattr(cls, name, None)
            if callable(fn):
                try:
                    if name == "from_json":
                        return fn(json.dumps(data))
                    return fn(data)
                except Exception:
                    pass
        # Try plain constructor
        try:
            return cls(**data)
        except Exception:
            pass
        return None

    def _import_default_session_class(self) -> Any:
        # Attempt to import a symbol named 'Session' from the calling context if available.
        # This is a best-effort heuristic.
        try:
            # Try common modules
            for mod_name in ("__main__",):
                try:
                    mod = importlib.import_module(mod_name)
                    if hasattr(mod, "Session"):
                        return getattr(mod, "Session")
                except Exception:
                    continue
        except Exception:
            pass
        raise ImportError(
            "Unable to locate a default Session class for hydration")
