from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    # Only for type checking; runtime access will use globals().get('Session')
    from typing import Optional
    from . import Session  # type: ignore[unused-ignore]


class JSONSessionSerializer:
    '''Serialize and deserialize ADK Session to/from JSON.
    Notes: this is not a complete serializer. It saves and reads
    only a necessary subset of fields.
    '''

    def __init__(self, storage_path: Path) -> None:
        '''Initialize a new instance of JSONSessionSerializer.'''
        self.storage_path = Path(storage_path)

    def _file_path(self, *, app_name: str | None = None, user_id: str | None = None, session_id: str | None = None, session: 'Session | None' = None) -> Path:
        '''Construct the JSON file path for a session.'''

        def _deep_get(obj: Any, *names: str) -> Any | None:
            for name in names:
                cur = obj
                ok = True
                for part in name.split('.'):
                    if cur is None:
                        ok = False
                        break
                    cur = getattr(cur, part, None)
                if ok and cur is not None:
                    return cur
            return None

        if session is not None:
            app_name = app_name or _deep_get(session, 'app_name', 'app.name')
            user_id = user_id or _deep_get(
                session, 'user_id', 'user.id', 'uid', 'userId')
            session_id = session_id or _deep_get(
                session, 'session_id', 'id', 'sid', 'uuid')

        if not app_name or not user_id or not session_id:
            raise ValueError(
                'app_name, user_id and session_id are required to build a file path')

        # Normalize to string
        app_name = str(app_name)
        user_id = str(user_id)
        session_id = str(session_id)

        return self.storage_path / app_name / user_id / f'{session_id}.json'

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
                payload = json.load(f)
        except Exception:
            return None

        # Backward/forward compatible minimal fields
        meta = payload if isinstance(payload, dict) else {}
        data = meta.get('payload') if isinstance(
            meta.get('payload'), dict) else meta

        # Ensure required basics exist
        data.setdefault('app_name', meta.get('app_name', app_name))
        data.setdefault('user_id', meta.get('user_id', user_id))
        data.setdefault('session_id', meta.get('session_id', session_id))

        # Try to construct a Session instance using common patterns
        SessionCls = globals().get('Session')

        if SessionCls is None:
            # Can't construct proper Session; return None as we can't satisfy type
            return None

        # Try common constructors in order of preference
        try_constructors = [
            # method expects JSON string
            ('from_json', (json.dumps(payload),), {}),
            ('from_dict', (payload,), {}),
            ('from_dict', (data,), {}),
            ('model_validate', (payload,), {}),  # pydantic v2
            ('parse_obj', (payload,), {}),       # pydantic v1
        ]

        for meth, args, kwargs in try_constructors:
            fn = getattr(SessionCls, meth, None)
            if callable(fn):
                try:
                    return fn(*args, **kwargs)  # type: ignore[misc]
                except Exception:
                    pass

        # Try direct construction with full payload
        try:
            return SessionCls(**payload)  # type: ignore[misc]
        except Exception:
            pass

        # Try direct construction with minimal data
        try:
            return SessionCls(
                app_name=data.get('app_name'),
                user_id=data.get('user_id'),
                session_id=data.get('session_id'),
            )  # type: ignore[misc]
        except Exception:
            pass

        # As a last resort, try empty constructor and set attributes
        try:
            obj = SessionCls()  # type: ignore[misc]
            for k, v in data.items():
                try:
                    setattr(obj, k, v)
                except Exception:
                    pass
            return obj
        except Exception:
            return None

    def write(self, session: 'Session') -> Path:
        '''Write a session to a JSON file.'''
        path = self._file_path(session=session)

        # Build payload: minimal fields plus an optional serialized payload
        def _maybe_call(obj: Any, name: str) -> Any | None:
            fn = getattr(obj, name, None)
            if callable(fn):
                try:
                    return fn()
                except Exception:
                    return None
            return None

        # Prefer dict-like outputs if available
        payload: dict[str, Any] = {}
        dict_like = None
        # Try common serialization methods
        for method in ('to_dict', 'dict', 'model_dump'):
            dict_like = _maybe_call(session, method)
            if isinstance(dict_like, dict):
                break
        if isinstance(dict_like, dict):
            payload_data = dict_like
        else:
            # Fallback: reflect __dict__
            payload_data = getattr(session, '__dict__', {}) or {}

        # Minimal explicit fields
        def _deep_get(obj: Any, *names: str) -> Any | None:
            for name in names:
                cur = obj
                ok = True
                for part in name.split('.'):
                    if cur is None:
                        ok = False
                        break
                    cur = getattr(cur, part, None)
                if ok and cur is not None:
                    return cur
            return None

        app_name = _deep_get(session, 'app_name', 'app.name')
        user_id = _deep_get(session, 'user_id', 'user.id', 'uid', 'userId')
        session_id = _deep_get(session, 'session_id', 'id', 'sid', 'uuid')

        meta: dict[str, Any] = {
            'app_name': app_name,
            'user_id': user_id,
            'session_id': session_id,
            'payload': payload_data,
            'serializer': 'json',
            'version': 1,
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2, sort_keys=True)
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
        base = self.storage_path / app_name / user_id
        if not base.exists():
            return iter(())
        sessions: list['Session'] = []
        for file in sorted(base.glob('*.json')):
            s = self.read(app_name, user_id, file.stem)
            if s is not None:
                sessions.append(s)
        return iter(sessions)
