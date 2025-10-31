
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
        self.actions = actions if actions is not None else []
        self.strict = strict
        self.directory = directory

    def modify(self, modification, obj) -> None:
        if isinstance(obj, dict):
            self.modify_object(modification, obj)
        else:
            raise NotImplementedError(
                "Modification of non-dict objects is not implemented.")

    def modify_object(self, modification, obj):
        for action_key, action_value in modification.items():
            if action_key.startswith('_'):
                action_name = action_key[1:]
                for action_class in self.actions:
                    if action_class.__name__.lower() == action_name.lower():
                        action_instance = action_class(
                            self.strict, self.directory)
                        action_instance.apply(action_value, obj)
                        break
                else:
                    if self.strict:
                        raise ValueError(f"Unknown action: {action_name}")
            else:
                if action_key in obj and isinstance(obj[action_key], dict) and isinstance(action_value, dict):
                    self.modify_object(action_value, obj[action_key])
                else:
                    obj[action_key] = action_value
