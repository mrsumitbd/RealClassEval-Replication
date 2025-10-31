from __future__ import annotations

import base64
import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path
from types import SimpleNamespace
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
            app_name = app_name or getattr(session, 'app_name', None)
            user_id = user_id or getattr(session, 'user_id', None)
            session_id = session_id or getattr(
                session, 'session_id', None) or getattr(session, 'id', None)

        if not app_name or not user_id or not session_id:
            raise ValueError(
                'app_name, user_id, and session_id are required to construct file path')

        return self.storage_path / app_name / user_id / f'{session_id}.json'

    def read(self, app_name: str, user_id: str, session_id: str) -> 'Session | None':
        '''Read a session from a JSON file.
        The config parameter is currently not used for filtering during read.
        '''
        fpath = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        if not fpath.exists():
            return None
        try:
            with fpath.open('r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return None

        if isinstance(data, dict):
            # Common wrappers
            if 'session' in data and isinstance(data['session'], dict):
                data = data['session']
        else:
            return None

        # Ensure identifiers are present
        data.setdefault('app_name', app_name)
        data.setdefault('user_id', user_id)
        data.setdefault('session_id', session_id)

        return self._construct_session(data)

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        fpath = self._file_path(session=session)
        fpath.parent.mkdir(parents=True, exist_ok=True)

        data = self._extract_session_data(session)
        # Ensure identifiers present
        data['app_name'] = data.get('app_name') or getattr(
            session, 'app_name', None)
        data['user_id'] = data.get('user_id') or getattr(
            session, 'user_id', None)
        data['session_id'] = data.get('session_id') or getattr(
            session, 'session_id', None) or getattr(session, 'id', None)
        # Minimal metadata
        data.setdefault('updated_at', datetime.utcnow().isoformat())

        json_data = self._to_jsonable(data)

        tmp_path = fpath.with_suffix('.json.tmp')
        with tmp_path.open('w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False,
                      indent=2, sort_keys=True)
        tmp_path.replace(fpath)
        return fpath

    def delete(self, app_name: str, user_id: str, session_id: str) -> None:
        '''Delete a session's JSON file.'''
        fpath = self._file_path(
            app_name=app_name, user_id=user_id, session_id=session_id)
        try:
            fpath.unlink()
        except FileNotFoundError:
            return
        # Optional: cleanup empty directories
        for parent in (fpath.parent, fpath.parent.parent):
            try:
                parent.rmdir()
            except OSError:
                break

    def list_saved(self, *, app_name: str, user_id: str) -> 'Iterator[Session]':
        '''List saved sessions.'''
        base = self.storage_path / app_name / user_id
        if not base.exists():
            return iter(())

        def _gen() -> Iterator['Session']:
            for p in sorted(base.glob('*.json')):
                sid = p.stem
                sess = self.read(app_name, user_id, sid)
                if sess is not None:
                    yield sess
        return _gen()

    # Helpers

    def _extract_session_data(self, session: Any) -> dict[str, Any]:
        # Prefer explicit model dumpers
        for attr in ('to_dict', 'model_dump', 'dict'):
            fn = getattr(session, attr, None)
            if callable(fn):
                try:
                    data = fn()  # type: ignore[misc]
                    if isinstance(data, Mapping):
                        return dict(data)
                except Exception:
                    pass
        if is_dataclass(session):
            try:
                return asdict(session)
            except Exception:
                pass

        # Fallback: pick a minimal subset of likely fields
        candidates = {}
        if hasattr(session, '__dict__'):
            candidates = {k: v for k, v in vars(
                session).items() if not k.startswith('_')}
        # Whitelist of commonly needed fields
        whitelist = {
            'app_name', 'user_id', 'session_id', 'id',
            'created_at', 'updated_at', 'created', 'updated',
            'title', 'name', 'summary', 'description',
            'config', 'settings', 'metadata', 'meta',
            'messages', 'history', 'thread',
        }
        minimal = {k: candidates[k] for k in candidates.keys() & whitelist}
        # Guarantee identifiers if available via properties
        minimal.setdefault('app_name', getattr(session, 'app_name', None))
        minimal.setdefault('user_id', getattr(session, 'user_id', None))
        minimal.setdefault('session_id', getattr(
            session, 'session_id', None) or getattr(session, 'id', None))
        return minimal

    def _to_jsonable(self, obj: Any) -> Any:
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, (datetime, date, time)):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.value if hasattr(obj, 'value') else obj.name
        if isinstance(obj, bytes):
            return {'__type__': 'bytes', 'base64': base64.b64encode(obj).decode('ascii')}
        if isinstance(obj, Mapping):
            return {str(k): self._to_jsonable(v) for k, v in obj.items() if v is not None}
        if isinstance(obj, (list, tuple, set)):
            return [self._to_jsonable(v) for v in obj]
        if is_dataclass(obj):
            return self._to_jsonable(asdict(obj))
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            try:
                return self._to_jsonable(obj.to_dict())
            except Exception:
                pass
        if hasattr(obj, 'model_dump') and callable(getattr(obj, 'model_dump')):
            try:
                return self._to_jsonable(obj.model_dump())
            except Exception:
                pass
        if hasattr(obj, '__dict__'):
            data = {k: v for k, v in vars(
                obj).items() if not k.startswith('_')}
            return self._to_jsonable(data)
        return str(obj)

    def _construct_session(self, data: dict[str, Any]) -> 'Session':
        SessionCls = None
        # Try common import locations
        try:
            from .session import Session as _Session  # type: ignore
            SessionCls = _Session
        except Exception:
            try:
                from session import Session as _Session  # type: ignore
                SessionCls = _Session
            except Exception:
                SessionCls = None

        if SessionCls is not None:
            # Try common constructors
            try:
                if hasattr(SessionCls, 'from_dict') and callable(getattr(SessionCls, 'from_dict')):
                    # type: ignore[attr-defined]
                    return SessionCls.from_dict(data)
            except Exception:
                pass
            try:
                if hasattr(SessionCls, 'model_validate') and callable(getattr(SessionCls, 'model_validate')):
                    # type: ignore[attr-defined]
                    return SessionCls.model_validate(data)
            except Exception:
                pass
            try:
                if hasattr(SessionCls, 'parse_obj') and callable(getattr(SessionCls, 'parse_obj')):
                    # type: ignore[attr-defined]
                    return SessionCls.parse_obj(data)
            except Exception:
                pass
            try:
                return SessionCls(**data)  # type: ignore[misc]
            except Exception:
                pass

        # Fallback to a simple namespace
        return SimpleNamespace(**data)  # type: ignore[return-value]
