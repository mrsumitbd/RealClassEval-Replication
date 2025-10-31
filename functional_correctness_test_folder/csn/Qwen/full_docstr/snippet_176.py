
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
        self.actions = actions if actions is not None else []
        self.strict = strict
        self.directory = directory

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
        for action_key, settings in modification.items():
            action_class = next(
                (action for action in self.actions if action.key == action_key), None)
            if action_class:
                action = action_class()
                action.apply(obj, settings)
            elif self.strict:
                raise ValueError(f"Unsupported action: {action_key}")

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        obj_dict = obj.as_dict()
        self.modify(modification, obj_dict)
        obj.__init__(**obj_dict)
