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
        self.strict = strict
        self.directory = directory

        # Registry: keyword -> callable(modder, obj, settings)
        self._actions = {}

        # Built-in actions
        self._register_builtin('_set', self._action_set)
        self._register_builtin('_unset', self._action_unset)
        self._register_builtin('_inc', self._action_inc)
        self._register_builtin('_push', self._action_push)
        self._register_builtin('_pull', self._action_pull)

        # External/custom actions (optional)
        if actions:
            for act in actions:
                inst = act() if isinstance(act, type) else act
                kw = getattr(inst, 'keyword', None)
                apply_fn = getattr(inst, 'apply', None)
                if not kw or not callable(apply_fn):
                    if self.strict:
                        raise ValueError(
                            "Action must define 'keyword' and callable 'apply'")
                    else:
                        continue
                # Wrap to pass self for helper usage if the apply expects 3 args

                def make_wrapper(f):
                    def wrapper(modder, obj, settings, _f=f):
                        # Try signatures (modder, obj, settings) or (obj, settings)
                        try:
                            return _f(modder, obj, settings)
                        except TypeError:
                            return _f(obj, settings)
                    return wrapper
                self._actions[kw] = make_wrapper(apply_fn)

    def modify(self, modification, obj) -> None:
        if not isinstance(modification, dict):
            raise TypeError("modification must be a dict of actions")

        # Object path if it implements as_dict/from_dict
        if hasattr(obj, 'as_dict') and callable(getattr(obj, 'as_dict')) and \
           hasattr(obj.__class__, 'from_dict') and callable(getattr(obj.__class__, 'from_dict')):
            # Modify via dict representation and return new object
            new_obj = self.modify_object(modification, obj)
            # If caller passed a dict-like object container, we cannot replace in-place here.
            # Caller should use modify_object's return value.
            return new_obj

        # Directly modify dicts
        if isinstance(obj, dict):
            for action_kw, settings in modification.items():
                action = self._actions.get(action_kw)
                if action is None:
                    if self.strict:
                        raise KeyError(f"Unknown action keyword: {action_kw}")
                    else:
                        continue
                action(self, obj, settings)
            return None

        # Unsupported object without as_dict/from_dict contract
        if self.strict:
            raise TypeError(
                "Object must be a dict or support as_dict()/from_dict()")
        return None

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        if not (hasattr(obj, 'as_dict') and callable(getattr(obj, 'as_dict')) and
                hasattr(obj.__class__, 'from_dict') and callable(getattr(obj.__class__, 'from_dict'))):
            if self.strict:
                raise TypeError(
                    "Object must support as_dict() and from_dict()")
            return obj

        d = obj.as_dict()
        self.modify(modification, d)
        # Return a new instance based on modified dict
        return obj.__class__.from_dict(d)

    # ----------------------
    # Built-in action impls
    # ----------------------
    def _register_builtin(self, keyword, func):
        self._actions[keyword] = func

    def _action_set(self, obj, settings):
        if not isinstance(settings, dict):
            raise TypeError("_set requires a dict of path: value")
        for path, value in settings.items():
            self._set_path_value(obj, path, value, create=True)

    def _action_unset(self, obj, settings):
        # settings can be dict with flags or list/tuple of paths
        paths = []
        if isinstance(settings, dict):
            paths = [p for p, flag in settings.items() if flag]
        elif isinstance(settings, (list, tuple, set)):
            paths = list(settings)
        else:
            raise TypeError("_unset requires dict or list of paths")
        for path in paths:
            self._unset_path(obj, path)

    def _action_inc(self, obj, settings):
        if not isinstance(settings, dict):
            raise TypeError("_inc requires a dict of path: number")
        for path, inc_by in settings.items():
            parent, key = self._traverse_to_parent(obj, path, create=True)
            current = self._get_from_parent(parent, key, default=0)
            try:
                new_val = current + inc_by
            except Exception as e:
                if self.strict:
                    raise TypeError(
                        f"Cannot increment non-numeric value at {path}: {e}")
                else:
                    continue
            self._set_in_parent(parent, key, new_val)

    def _action_push(self, obj, settings):
        # settings: dict of path: value_to_append or path: [values] to extend
        if not isinstance(settings, dict):
            raise TypeError("_push requires a dict of path: value")
        for path, to_add in settings.items():
            parent, key = self._traverse_to_parent(obj, path, create=True)
            lst = self._get_from_parent(parent, key, default=None)
            if lst is None:
                lst = []
            if not isinstance(lst, list):
                if self.strict:
                    raise TypeError(f"_push target at {path} is not a list")
                else:
                    continue
            if isinstance(to_add, list):
                lst.extend(to_add)
            else:
                lst.append(to_add)
            self._set_in_parent(parent, key, lst)

    def _action_pull(self, obj, settings):
        # settings: dict of path: value_to_remove; removes equal elements
        if not isinstance(settings, dict):
            raise TypeError("_pull requires a dict of path: value")
        for path, to_remove in settings.items():
            parent, key = self._traverse_to_parent(obj, path, create=False)
            if parent is None:
                if self.strict:
                    raise KeyError(f"Path not found for _pull: {path}")
                continue
            lst = self._get_from_parent(parent, key, default=None)
            if not isinstance(lst, list):
                if self.strict:
                    raise TypeError(f"_pull target at {path} is not a list")
                else:
                    continue
            lst = [x for x in lst if x != to_remove]
            self._set_in_parent(parent, key, lst)

    # ----------------------
    # Path helpers
    # ----------------------
    def _split_path(self, path):
        if isinstance(path, (list, tuple)):
            parts = list(path)
        elif isinstance(path, str):
            parts = path.split('.') if path else []
        else:
            parts = [path]
        return [self._coerce_index(p) for p in parts]

    @staticmethod
    def _coerce_index(token):
        # Convert numeric strings to int for list indexing
        if isinstance(token, str):
            if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
                try:
                    return int(token)
                except Exception:
                    return token
        return token

    def _traverse_to_parent(self, obj, path, create=False):
        parts = self._split_path(path)
        if not parts:
            return None, None
        cur = obj
        for i, part in enumerate(parts[:-1]):
            nxt = self._get_child(cur, part)
            if nxt is None:
                if not create:
                    return None, None
                nxt = [] if isinstance(parts[i+1], int) else {}
                self._set_child(cur, part, nxt)
            cur = nxt
        return cur, parts[-1]

    def _get_child(self, container, key):
        if isinstance(key, int):
            if isinstance(container, list):
                if -len(container) <= key < len(container):
                    return container[key]
                return None
            return None
        else:
            if isinstance(container, dict):
                return container.get(key, None)
            return None

    def _set_child(self, container, key, value):
        if isinstance(key, int):
            if not isinstance(container, list):
                if self.strict:
                    raise TypeError(
                        "Trying to set list index on non-list container")
                return
            # Extend list as needed
            idx = key
            if idx < 0:
                # Support negative indices by converting to positive position
                idx = len(container) + idx
            if idx < 0:
                # Prepend with None to reach index 0
                container[:0] = [None] * (-idx)
                idx = 0
            if idx >= len(container):
                container.extend([None] * (idx - len(container) + 1))
            container[key] = value
        else:
            if not isinstance(container, dict):
                if self.strict:
                    raise TypeError(
                        "Trying to set dict key on non-dict container")
                return
            container[key] = value

    def _get_from_parent(self, parent, key, default=None):
        if isinstance(key, int):
            if isinstance(parent, list) and -len(parent) <= key < len(parent):
                return parent[key]
            return default
        else:
            if isinstance(parent, dict):
                return parent.get(key, default)
            return default

    def _set_in_parent(self, parent, key, value):
        self._set_child(parent, key, value)

    def _set_path_value(self, obj, path, value, create=True):
        parent, key = self._traverse_to_parent(obj, path, create=create)
        if parent is None:
            if self.strict:
                raise KeyError(f"Path not found: {path}")
            return
        self._set_in_parent(parent, key, value)

    def _unset_path(self, obj, path):
        parent, key = self._traverse_to_parent(obj, path, create=False)
        if parent is None:
            if self.strict:
                raise KeyError(f"Path not found: {path}")
            return
        if isinstance(key, int):
            if isinstance(parent, list):
                if -len(parent) <= key < len(parent):
                    # Remove element to shift left, mimicking pull by index
                    parent.pop(key)
                elif self.strict:
                    raise IndexError(
                        f"Index out of range for _unset at {path}")
        else:
            if isinstance(parent, dict):
                if key in parent:
                    del parent[key]
                elif self.strict:
                    raise KeyError(f"Key not found for _unset at {path}")
