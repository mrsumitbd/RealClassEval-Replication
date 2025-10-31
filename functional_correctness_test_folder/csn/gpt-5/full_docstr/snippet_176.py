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

    class _DefaultDictActions:
        ALLOWED_ACTIONS = {
            "_set": "set",
            "_unset": "unset",
        }

        def __init__(self, directory="./") -> None:
            self.directory = directory

        def set(self, dct, settings):
            if not isinstance(dct, dict):
                raise TypeError(
                    "Default DictActions only operate on dict objects.")
            if not isinstance(settings, dict):
                raise TypeError("_set requires a dict of key: value pairs.")
            for k, v in settings.items():
                dct[k] = v

        def unset(self, dct, settings):
            if not isinstance(dct, dict):
                raise TypeError(
                    "Default DictActions only operate on dict objects.")
            keys = []
            if isinstance(settings, dict):
                keys = [k for k, v in settings.items() if v]
            elif isinstance(settings, (list, tuple, set)):
                keys = list(settings)
            elif isinstance(settings, str):
                keys = [settings]
            else:
                raise TypeError(
                    "_unset requires a dict/list/str of keys to remove.")
            for k in keys:
                if k in dct:
                    del dct[k]

    def __init__(self, actions=None, strict=True, directory='./') -> None:
        '''Initialize a Modder from a list of supported actions.
        Args:
            actions ([Action]): A sequence of supported actions. See
                :mod:`custodian.ansible.actions`. Default is None,
                which means only DictActions are supported.
            strict (bool): Indicating whether to use strict mode. In non-strict
                mode, unsupported actions are simply ignored without any
                errors raised. In strict mode, if an unsupported action is
                supplied, a ValueError is raised. Defaults to True.
            directory (str): The directory containing the files to be modified.
                Defaults to "./".
        '''
        self.directory = directory
        self.strict = bool(strict)
        if actions is None:
            action_classes = [self._DefaultDictActions]
        else:
            action_classes = list(actions)

        self._actions = []
        for cls in action_classes:
            try:
                self._actions.append(cls(self.directory))
            except TypeError:
                # Fallback if the action does not accept directory
                self._actions.append(cls())

    def _apply_with_action(self, action_obj, action_key, settings, obj):
        # 1) Preferred: ALLOWED_ACTIONS mapping
        mapping = getattr(action_obj, "ALLOWED_ACTIONS", None)
        if isinstance(mapping, dict) and action_key in mapping:
            method_name = mapping[action_key]
            method = getattr(action_obj, method_name, None)
            if callable(method):
                method(obj, settings)
                return True

        # 2) Fallback: method with underscored key removed, e.g. "_set" -> "set"
        plain_name = action_key.lstrip("_")
        method = getattr(action_obj, plain_name, None)
        if callable(method):
            method(obj, settings)
            return True

        # 3) Fallback: generic apply(action_key, settings, obj)
        apply_method = getattr(action_obj, "apply", None)
        if callable(apply_method):
            result = apply_method(action_key, settings, obj)
            # If apply does not indicate success, assume it succeeded by not raising.
            return True if result is None else bool(result)

        return False

    def modify(self, modification, obj) -> None:
        '''
        Note that modify makes actual in-place modifications. It does not
        return a copy.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (dict/str/object): Object to modify depending on actions. For
                example, for DictActions, obj will be a dict to be modified.
                For FileActions, obj will be a string with a full pathname to a
                file.
        '''
        if not isinstance(modification, dict):
            raise TypeError(
                "modification must be a dict of {action_keyword: settings}.")

        for action_key, settings in modification.items():
            matched = False
            for action in self._actions:
                if self._apply_with_action(action, action_key, settings, obj):
                    matched = True
                    break
            if not matched and self.strict:
                raise ValueError(
                    f"Unsupported action '{action_key}' for supplied actions.")

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        if not hasattr(obj, "as_dict"):
            raise TypeError("Object must implement as_dict().")
        if not hasattr(obj.__class__, "from_dict"):
            raise TypeError("Object's class must implement from_dict(d).")

        dct = obj.as_dict()
        self.modify(modification, dct)
        return obj.__class__.from_dict(dct)
