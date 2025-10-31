
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
        # Build action keyword to action class mapping
        self._action_map = {}
        for action in self.actions:
            if hasattr(action, 'keyword'):
                self._action_map[action.keyword] = action
            elif hasattr(action, '__name__'):
                # fallback: use class name as keyword, e.g. _set
                self._action_map['_' +
                                 action.__name__.replace('Action', '').lower()] = action

    def modify(self, modification, obj) -> None:
        if not isinstance(modification, dict):
            raise ValueError("Modification must be a dict")
        for key, value in modification.items():
            if key not in self._action_map:
                if self.strict:
                    raise ValueError(f"Unknown action keyword: {key}")
                else:
                    continue
            action_cls = self._action_map[key]
            action = action_cls()
            action.apply(obj, value)

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        dct = obj.as_dict()
        self.modify(modification, dct)
        # Assume from_dict is a classmethod
        new_obj = obj.__class__.from_dict(dct)
        # Update obj in-place if possible
        if hasattr(obj, '__dict__'):
            obj.__dict__.update(new_obj.__dict__)
        return obj

    class _SetAction:
        keyword = '_set'

        def apply(self, obj, settings):
            for k, v in settings.items():
                obj[k] = v
