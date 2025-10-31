from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, Mapping


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        # Try to locate a Session class for reconstruction, if available.
        self._SessionClass = None
        for modpath in (
            'session',
            '.session',
            'adk.session',
            'app.session',
        ):
            try:
                if modpath.startswith('.'):
                    # Relative import won't work reliably here without package context
                    continue
                module = __import__(modpath, fromlist=['Session'])
                if hasattr(module, 'Session'):
                    self._SessionClass = getattr(module, 'Session')
                    break
            except Exception:
                continue

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        '''Construct the JSON file path for a session.'''
        def _get(obj: Any, key: str) -> Any:
            if obj is None:
                return None
            if hasattr(obj, key):
                return getattr(obj, key)
            if isinstance(obj, Mapping):
                return obj.get(key)
            return None

        app = app_name or _get(session, 'app_name')
        user = user_id or _get(session, 'user_id')
        sid = session_id or _get(session, 'session_id')

        if not app or not user or not sid:
            raise ValueError(
                'app_name, user_id, and session_id are required to build the file path')

        return self.storage_path / str(app) / str(user) / f'{sid}.json'

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not path.exists():
            return None
        try:
            with path.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return None
        return self._construct_session(data)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        path = self._file_path(session=session)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = self._extract_session_data(session)
        tmp = path.with_suffix('.json.tmp')
        with tmp.open('w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False,
                      separators=(',', ':'), sort_keys=True)
        tmp.replace(path)
        return path

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        path = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            path.unlink()
        except FileNotFoundError:
            pass

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        base = self.storage_path / str(app_name) / str(user_id)
        if not base.exists() or not base.is_dir():
            return iter(())

        def _gen() -> Iterator['Session']:
            for p in sorted(base.glob('*.json')):
                try:
                    with p.open('r', encoding='utf-8') as f:
                        data = json.load(f)
                    sess = self._construct_session(data)
                    if sess is not None:
                        yield sess
                except Exception:
                    continue
        return _gen()

    # Helpers

    def _extract_session_data(self, session: Any) -> dict[str, Any]:
        # Use minimal, broadly named fields if present
        fields_preference = [
            'app_name',
            'user_id',
            'user',
            'session_id',
            'id',
            'name',
            'title',
            'description',
            'status',
            'state',
            'created_at',
            'updated_at',
            'metadata',
            'config',
            'data',
            'params',
            'labels',
            'extra',
        ]

        def _get(obj: Any, key: str) -> Any:
            if hasattr(obj, key):
                return getattr(obj, key)
            if isinstance(obj, Mapping):
                return obj.get(key)
            # pydantic models
            if hasattr(obj, 'model_dump'):
                try:
                    # type: ignore[attr-defined]
                    return obj.model_dump().get(key)
                except Exception:
                    pass
            if hasattr(obj, 'dict'):
                try:
                    return obj.dict().get(key)  # type: ignore[attr-defined]
                except Exception:
                    pass
            return None

        # Start with a small dictionary
        data: dict[str, Any] = {}

        # Try to get essential identifiers
        app = _get(session, 'app_name')
        user = _get(session, 'user_id') or _get(session, 'user')
        sid = _get(session, 'session_id') or _get(session, 'id')

        if app is not None:
            data['app_name'] = app
        if user is not None:
            data['user_id'] = user
        if sid is not None:
            data['session_id'] = sid

        # Optional fields
        for k in fields_preference:
            if k in ('app_name', 'user_id', 'user', 'session_id', 'id'):
                continue
            v = _get(session, k)
            if v is not None:
                data[k] = v

        # Fallback for wide export if available
        wide = None
        if hasattr(session, 'to_dict'):
            try:
                wide = session.to_dict()  # type: ignore[attr-defined]
            except Exception:
                wide = None
        if wide is None and hasattr(session, 'model_dump'):
            try:
                wide = session.model_dump()  # type: ignore[attr-defined]
            except Exception:
                wide = None
        if wide is None and hasattr(session, 'dict'):
            try:
                wide = session.dict()  # type: ignore[attr-defined]
            except Exception:
                wide = None
        # If wide exists, merge only unknown keys to keep minimal set
        if isinstance(wide, Mapping):
            for k, v in wide.items():
                if k not in data:
                    data[k] = v

        # Serializer metadata
        data['_serializer'] = 'json'
        data['_version'] = 1

        return self._to_jsonable(data)

    def _to_jsonable(self, obj: Any) -> Any:
        # Convert objects to json-serializable equivalents
        import datetime
        from enum import Enum
        from pathlib import Path as _P
        from uuid import UUID

        if obj is None:
            return None
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, (list, tuple, set)):
            return [self._to_jsonable(x) for x in obj]
        if isinstance(obj, dict):
            return {str(self._to_jsonable(k)): self._to_jsonable(v) for k, v in obj.items()}
        if isinstance(obj, _P):
            return str(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return getattr(obj, 'value', obj.name)
        if isinstance(obj, datetime.datetime):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)
        if isinstance(obj, datetime.date):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)
        # Try custom serialization hooks
        if hasattr(obj, 'to_dict'):
            try:
                return self._to_jsonable(obj.to_dict())
            except Exception:
                pass
        if hasattr(obj, 'model_dump'):
            try:
                # type: ignore[attr-defined]
                return self._to_jsonable(obj.model_dump())
            except Exception:
                pass
        if hasattr(obj, '__dict__'):
            try:
                return self._to_jsonable(vars(obj))
            except Exception:
                pass
        return str(obj)

    def _construct_session(self, data: dict[str, Any]) -> 'Session | None':
        # Prefer a Session class if we could import one
        cls = self._SessionClass
        if cls is not None:
            # Try common constructors
            try:
                if hasattr(cls, 'from_dict'):
                    return cls.from_dict(data)  # type: ignore[attr-defined]
            except Exception:
                pass
            try:
                if hasattr(cls, 'from_json'):
                    return cls.from_json(data)  # type: ignore[attr-defined]
            except Exception:
                pass
            try:
                return cls(**data)  # type: ignore[call-arg]
            except Exception:
                # Try minimal constructor and then set attributes
                try:
                    kwargs = {}
                    for k in ('app_name', 'user_id', 'session_id'):
                        if k in data:
                            kwargs[k] = data[k]
                    obj = cls(**kwargs)  # type: ignore[call-arg]
                    for k, v in data.items():
                        try:
                            setattr(obj, k, v)
                        except Exception:
                            pass
                    return obj
                except Exception:
                    pass
        # Fallback: return data as-is wrapped to look like an object
        try:
            from types import SimpleNamespace
            return SimpleNamespace(**data)  # type: ignore[return-value]
        except Exception:
            return None
