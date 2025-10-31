class Modder:
    '''
    Class to modify a dict/file/any object using a mongo-like language.
    Keywords are mostly adopted from mongo's syntax, but instead of $, an
    underscore precedes action keywords. This is so that the modification can
    be inserted into a mongo db easily.
    Allowable actions are supplied as a list of classes as an argument. Refer
    to the action classes on what the actions do. Action classes are in
    pymatpro.ansible.actions.
    Examples:
    >>> modder = Modder()
    >>> dct = {"Hello": "World"}
    >>> mod = {'_set': {'Hello':'Universe', 'Bye': 'World'}}
    >>> modder.modify(mod, dct)
    >>> dct['Bye']
    'World'
    >>> dct['Hello']
    'Universe'
    '''

    def __init__(self, actions=None, strict=True, directory='./') -> None:
        self.strict = bool(strict)
        self.directory = directory
        self._actions = {}

        # Register built-in default actions
        self._register_action('_set', self._act_set)
        self._register_action('_unset', self._act_unset)
        self._register_action('_inc', self._act_inc)
        self._register_action('_push', self._act_push)
        self._register_action('_extend', self._act_extend)
        self._register_action('_toggle', self._act_toggle)

        # Register additional actions if provided
        if actions:
            for act in actions:
                self._register_external_action(act)

    def modify(self, modification, obj) -> None:
        if modification is None:
            return
        if isinstance(modification, (list, tuple)):
            for m in modification:
                self.modify_object(m, obj)
        else:
            self.modify_object(modification, obj)

    def modify_object(self, modification, obj):
        if not isinstance(modification, dict):
            raise TypeError("Modification must be a dict or a list of dicts.")
        for key, payload in modification.items():
            if not isinstance(key, str) or not key.startswith('_'):
                # Skip non-action keys silently unless strict
                if self.strict:
                    raise KeyError(f"Unknown action: {key}")
                continue
            action = self._actions.get(key)
            if action is None:
                if self.strict:
                    raise KeyError(f"Unsupported action: {key}")
                continue
            action(obj, payload)

    # Action registration helpers

    def _register_action(self, keyword, func):
        self._actions[str(keyword)] = func

    def _register_external_action(self, action):
        # Accept:
        # - function with attribute 'keyword'/'key'/'name'
        # - class with class attribute 'keyword'/'key'/'name' and method 'apply'
        keyword = None
        apply_fn = None

        # Callable function
        if callable(action) and not isinstance(action, type):
            keyword = getattr(action, 'keyword', None) or getattr(
                action, 'key', None) or getattr(action, 'name', None)
            apply_fn = action

        # Class-like
        if keyword is None and isinstance(action, type):
            keyword = getattr(action, 'keyword', None) or getattr(
                action, 'key', None) or getattr(action, 'name', None)
            if hasattr(action, 'apply') and callable(getattr(action, 'apply')):
                inst = action()
                def apply_fn(target, payload, _inst=inst): return _inst.apply(
                    self, target, payload)

        if keyword is None or apply_fn is None:
            if self.strict:
                raise ValueError(
                    "Invalid action specification. Provide a callable with a keyword or a class with keyword and apply().")
            return

        keyword = str(keyword)
        if not keyword.startswith('_'):
            keyword = '_' + keyword

        # Wrap to uniform signature (obj, payload)
        def wrapper(target, payload, _fn=apply_fn):
            # External apply may have one of signatures:
            # - fn(modder, target, payload)
            # - fn(target, payload)
            try:
                return _fn(self, target, payload)
            except TypeError:
                return _fn(target, payload)

        self._register_action(keyword, wrapper)

    # Built-in action implementations

    def _act_set(self, target, payload):
        if not isinstance(payload, dict):
            raise TypeError("_set payload must be a dict of path: value")
        for path, value in payload.items():
            self._set_path(target, path, value)

    def _act_unset(self, target, payload):
        # payload can be list of paths or dict of path: True
        paths = []
        if isinstance(payload, dict):
            paths = [p for p, flag in payload.items(
            ) if flag or flag is None or flag is False]
        elif isinstance(payload, (list, tuple, set)):
            paths = list(payload)
        elif isinstance(payload, str):
            paths = [payload]
        else:
            raise TypeError("_unset payload must be a dict/list/str")
        for path in paths:
            self._del_path(target, path)

    def _act_inc(self, target, payload):
        if not isinstance(payload, dict):
            raise TypeError("_inc payload must be a dict of path: number")
        for path, inc in payload.items():
            cur = self._get_path(target, path, missing_sentinel=_MISSING)
            if cur is _MISSING:
                new_val = inc
            else:
                if not isinstance(inc, (int, float)):
                    raise TypeError("_inc value must be numeric")
                try:
                    new_val = cur + inc
                except Exception as e:
                    raise TypeError(
                        f"Cannot increment non-numeric at {path}: {e}")
            self._set_path(target, path, new_val)

    def _act_push(self, target, payload):
        # payload: dict path -> value (append)
        if not isinstance(payload, dict):
            raise TypeError("_push payload must be a dict of path: value")
        for path, value in payload.items():
            lst = self._get_path(target, path, missing_sentinel=_MISSING)
            if lst is _MISSING:
                lst = []
            if not isinstance(lst, list):
                raise TypeError(f"_push target at {path} is not a list")
            lst.append(value)
            self._set_path(target, path, lst)

    def _act_extend(self, target, payload):
        # payload: dict path -> iterable
        if not isinstance(payload, dict):
            raise TypeError("_extend payload must be a dict of path: iterable")
        for path, values in payload.items():
            lst = self._get_path(target, path, missing_sentinel=_MISSING)
            if lst is _MISSING:
                lst = []
            if not isinstance(lst, list):
                raise TypeError(f"_extend target at {path} is not a list")
            try:
                lst.extend(values)
            except TypeError:
                raise TypeError("_extend values must be iterable")
            self._set_path(target, path, lst)

    def _act_toggle(self, target, payload):
        # payload: dict path -> any (ignored) or list/str of paths
        paths = []
        if isinstance(payload, dict):
            paths = list(payload.keys())
        elif isinstance(payload, (list, tuple, set)):
            paths = list(payload)
        elif isinstance(payload, str):
            paths = [payload]
        else:
            raise TypeError("_toggle payload must be dict/list/str")
        for path in paths:
            cur = self._get_path(target, path, missing_sentinel=_MISSING)
            if cur is _MISSING:
                self._set_path(target, path, True)
            elif isinstance(cur, bool):
                self._set_path(target, path, not cur)
            else:
                raise TypeError(f"_toggle target at {path} is not boolean")

    # Path helpers

    def _split_path(self, path):
        if isinstance(path, (list, tuple)):
            parts = list(path)
        elif isinstance(path, str):
            parts = path.split('.') if path else []
        else:
            parts = [path]
        return [self._coerce_index(p) for p in parts if p != '']

    def _coerce_index(self, part):
        if isinstance(part, int):
            return part
        if isinstance(part, str) and part.isdigit():
            try:
                return int(part)
            except ValueError:
                return part
        return part

    def _is_mapping(self, obj):
        try:
            from collections.abc import Mapping
        except Exception:
            Mapping = dict
        return isinstance(obj, Mapping)

    def _get_from(self, obj, key, missing=_MISSING):
        if self._is_mapping(obj):
            return obj.get(key, missing)
        # list index
        if isinstance(obj, list) and isinstance(key, int):
            if -len(obj) <= key < len(obj):
                return obj[key]
            return missing
        # attribute
        if hasattr(obj, key):
            return getattr(obj, key)
        # fallback for __getitem__
        try:
            return obj[key]
        except Exception:
            return missing

    def _set_into(self, obj, key, value):
        if self._is_mapping(obj):
            obj[key] = value
            return
        if isinstance(obj, list) and isinstance(key, int):
            # expand list if needed
            if key < 0:
                raise IndexError("Negative indices not supported for set")
            if key >= len(obj):
                obj.extend([None] * (key - len(obj) + 1))
            obj[key] = value
            return
        # attribute if possible
        try:
            setattr(obj, key, value)
            return
        except Exception:
            pass
        # fallback to item assignment
        try:
            obj[key] = value
            return
        except Exception as e:
            raise TypeError(
                f"Cannot set key '{key}' on {type(obj).__name__}: {e}")

    def _del_from(self, obj, key):
        if self._is_mapping(obj):
            obj.pop(key, None)
            return
        if isinstance(obj, list) and isinstance(key, int):
            if -len(obj) <= key < len(obj):
                del obj[key]
            return
        if hasattr(obj, key):
            try:
                delattr(obj, key)
                return
            except Exception:
                pass
        try:
            del obj[key]
        except Exception:
            pass

    def _get_path(self, obj, path, missing_sentinel=None):
        parts = self._split_path(path)
        cur = obj
        for p in parts:
            cur = self._get_from(cur, p, missing=_MISSING)
            if cur is _MISSING:
                return missing_sentinel if missing_sentinel is not None else _MISSING
        return cur

    def _ensure_container(self, parent, key, next_key):
        val = self._get_from(parent, key, missing=_MISSING)
        if val is _MISSING or val is None:
            # choose dict for str keys, list for int keys
            container = [] if isinstance(next_key, int) else {}
            self._set_into(parent, key, container)
            return container
        return val

    def _set_path(self, obj, path, value):
        parts = self._split_path(path)
        if not parts:
            raise ValueError("Empty path")
        cur = obj
        for i, p in enumerate(parts[:-1]):
            nxt = parts[i + 1]
            # navigate or create
            existing = self._get_from(cur, p, missing=_MISSING)
            if existing is _MISSING or existing is None:
                existing = self._ensure_container(cur, p, nxt)
            cur = existing
        self._set_into(cur, parts[-1], value)

    def _del_path(self, obj, path):
        parts = self._split_path(path)
        if not parts:
            return
        cur = obj
        for p in parts[:-1]:
            cur = self._get_from(cur, p, missing=_MISSING)
            if cur is _MISSING:
                return
        self._del_from(cur, parts[-1])


class _Missing:
    pass


_MISSING = _Missing()
