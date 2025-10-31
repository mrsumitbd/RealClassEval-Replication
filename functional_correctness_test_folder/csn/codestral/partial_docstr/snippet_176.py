
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
            self.modify_dict(modification, obj)
        else:
            self.modify_object(modification, obj)

    def modify_dict(self, modification, dct):
        for action in self.actions:
            if action.keyword in modification:
                action(modification[action.keyword],
                       dct, self.strict, self.directory)

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        dct = obj.as_dict()
        self.modify_dict(modification, dct)
        obj.from_dict(dct)
