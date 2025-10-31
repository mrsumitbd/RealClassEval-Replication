
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
        # Default action: _set
        if actions is None:
            self.actions = [self._SetAction]
        else:
            self.actions = actions
        self.strict = strict
        self.directory = directory
        # Build action map: {'_set': <action class>, ...}
        self.action_map = {}
        for action in self.actions:
            if hasattr(action, 'keyword'):
                self.action_map[action.keyword] = action
            elif hasattr(action, '__name__'):
                # fallback: use class name, e.g. _SetAction -> '_set'
                name = action.__name__
                if name.startswith('_'):
                    key = name.lower()
                else:
                    key = '_' + \
                        name[0].lower(
                        ) + name[1:-6] if name.endswith('Action') else '_' + name.lower()
                self.action_map[key] = action

    def modify(self, modification, obj) -> None:
        if not isinstance(modification, dict):
            raise ValueError("Modification must be a dict")
        for key, value in modification.items():
            if key.startswith('_'):
                if key not in self.action_map:
                    if self.strict:
                        raise ValueError(f"Unknown action: {key}")
                    else:
                        continue
                action = self.action_map[key]()
                action.apply(obj, value)
            else:
                # Nested modification
                if isinstance(obj, dict) and key in obj:
                    self.modify(value, obj[key])
                elif hasattr(obj, key):
                    self.modify(value, getattr(obj, key))
                else:
                    if self.strict:
                        raise KeyError(f"Key {key} not found in object")
                    else:
                        continue

    def modify_object(self, modification, obj):
        self.modify(modification, obj)

    # Default _set action
    class _SetAction:
        keyword = '_set'

        def apply(self, obj, value):
            if isinstance(obj, dict):
                for k, v in value.items():
                    obj[k] = v
            else:
                for k, v in value.items():
                    setattr(obj, k, v)
