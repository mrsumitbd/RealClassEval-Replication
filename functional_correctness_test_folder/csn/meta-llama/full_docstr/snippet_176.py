
import os
from typing import Any, Dict, List, Optional, Sequence, Union


class Action:
    pass  # Assuming Action is defined elsewhere


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

    def __init__(self, actions: Optional[Sequence[Any]] = None, strict: bool = True, directory: str = './') -> None:
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
        self.supported_actions = actions if actions else []
        self.strict = strict
        self.directory = directory

    def modify(self, modification: Dict[str, Any], obj: Union[Dict, str, Any]) -> None:
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
        for action, settings in modification.items():
            found = False
            for a in self.supported_actions:
                if hasattr(a, 'keyword') and a.keyword == action:
                    a().modify(obj, settings, self.directory)
                    found = True
            if not found:
                if action.startswith('_'):
                    if self.strict:
                        raise ValueError(f'Unsupported action: {action}')
                else:
                    # Assuming DictActions is supported by default
                    from pymatpro.ansible.actions import DictActions
                    DictActions()._set(obj, {action: settings})

    def modify_object(self, modification: Dict[str, Any], obj: Any) -> None:
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        d = obj.as_dict()
        self.modify(modification, d)
        obj.__init__(**d)
