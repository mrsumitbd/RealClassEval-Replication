
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
        if isinstance(modification, dict):
            for key, value in modification.items():
                if key.startswith('_'):
                    self.modify_object({key: value}, obj)
                else:
                    if isinstance(obj, dict):
                        if key in obj:
                            self.modify(value, obj[key])
                        elif not self.strict:
                            obj[key] = value
                    elif hasattr(obj, key):
                        self.modify(value, getattr(obj, key))
                    elif not self.strict:
                        setattr(obj, key, value)
        else:
            raise ValueError("Modification must be a dictionary.")

    def modify_object(self, modification, obj):
        for action_key, action_value in modification.items():
            action_name = action_key[1:]  # Remove the underscore
            action_class = next(
                (a for a in self.actions if a.__name__.lower() == action_name.lower()), None)
            if action_class is not None:
                action = action_class()
                action.apply(obj, action_value)
            else:
                raise ValueError(f"Action '{action_name}' is not supported.")
