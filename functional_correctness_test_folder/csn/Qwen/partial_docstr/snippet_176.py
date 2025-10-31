
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
        self.actions = actions or []
        self.strict = strict
        self.directory = directory
        self.action_map = {action.keyword: action for action in self.actions}

    def modify(self, modification, obj) -> None:
        if isinstance(obj, dict):
            self._modify_dict(modification, obj)
        else:
            self.modify_object(modification, obj)

    def _modify_dict(self, modification, obj):
        for action_keyword, settings in modification.items():
            if action_keyword in self.action_map:
                action_class = self.action_map[action_keyword]
                action = action_class(
                    settings, strict=self.strict, directory=self.directory)
                action.apply(obj)
            elif self.strict:
                raise ValueError(f"Unknown action keyword: {action_keyword}")

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        obj_dict = obj.as_dict()
        self._modify_dict(modification, obj_dict)
        obj.from_dict(obj_dict)
