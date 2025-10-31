
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
            self._modify_dict(modification, obj)
        else:
            self.modify_object(modification, obj)

    def _modify_dict(self, modification, dct):
        for action, settings in modification.items():
            if action.startswith('_'):
                if action == '_set':
                    for k, v in settings.items():
                        dct[k] = v
                elif action == '_unset':
                    for k in settings:
                        if k in dct:
                            del dct[k]
                elif action == '_push':
                    for k, v in settings.items():
                        if k in dct and isinstance(dct[k], list):
                            dct[k].append(v)
                        elif not self.strict:
                            dct[k] = [v]
                elif action == '_inc':
                    for k, v in settings.items():
                        if k in dct and isinstance(dct[k], (int, float)):
                            dct[k] += v
                        elif not self.strict:
                            dct[k] = v
                else:
                    if self.strict:
                        raise ValueError(f"Unknown action: {action}")
            else:
                if self.strict:
                    raise ValueError(f"Action must start with '_': {action}")

    def modify_object(self, modification, obj):
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        from pymatgen.core import MSONable
        if isinstance(obj, MSONable):
            dct = obj.as_dict()
            self._modify_dict(modification, dct)
            obj = obj.from_dict(dct)
        else:
            raise ValueError("Object does not support as_dict/from_dict API")
