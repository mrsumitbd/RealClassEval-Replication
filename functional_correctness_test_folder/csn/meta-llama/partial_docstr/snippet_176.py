
import os
import importlib
from typing import Any, Dict, List, Optional


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

    def __init__(self, actions: Optional[List] = None, strict: bool = True, directory: str = './') -> None:
        self.supported_actions = self._get_supported_actions(
            actions, directory)
        self.strict = strict

    def _get_supported_actions(self, actions: Optional[List], directory: str) -> Dict:
        supported_actions = {}
        if actions is None:
            actions = []
            for file in os.listdir(os.path.join(directory, 'pymatpro/ansible/actions')):
                if file.endswith('.py') and file != '__init__.py':
                    module_name = file[:-3]
                    module = importlib.import_module(
                        f'pymatpro.ansible.actions.{module_name}')
                    for cls_name in dir(module):
                        cls = getattr(module, cls_name)
                        if isinstance(cls, type):
                            actions.append(cls)
        for action in actions:
            supported_actions[action.__name__] = action
        return supported_actions

    def modify(self, modification: Dict, obj: Any) -> None:
        for action, settings in modification.items():
            if action in self.supported_actions:
                self.supported_actions[action](self, obj, settings).apply()
            elif self.strict:
                raise ValueError(f'Unsupported action: {action}')

    def modify_object(self, modification: Dict, obj: Any) -> None:
        '''
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        '''
        dct = obj.as_dict()
        self.modify(modification, dct)
        obj.__init__(**dct)
