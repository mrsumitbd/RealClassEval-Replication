
class DictSetAction:
    keyword = "_set"

    @staticmethod
    def apply(settings, obj):
        for k, v in settings.items():
            obj[k] = v


class DictUnsetAction:
    keyword = "_unset"

    @staticmethod
    def apply(settings, obj):
        for k in settings:
            if k in obj:
                del obj[k]


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
        if actions is None:
            # Only support dict actions by default
            actions = [DictSetAction, DictUnsetAction]
        self._actions = {}
        for action in actions:
            self._actions[action.keyword] = action
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
        for action_keyword, settings in modification.items():
            action = self._actions.get(action_keyword)
            if action is not None:
                action.apply(settings, obj)
            elif self.strict:
                raise ValueError(f"Unsupported action: {action_keyword}")

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
        # Reconstruct the object in-place
        obj.__dict__.update(obj.__class__.from_dict(dct).__dict__)
