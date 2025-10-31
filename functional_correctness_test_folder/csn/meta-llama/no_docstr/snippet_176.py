
import os
import json
from importlib import import_module


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
        self.directory = directory
        self.strict = strict
        if actions is None:
            actions = []
            for file in os.listdir(os.path.join(os.path.dirname(__file__), 'actions')):
                if file.endswith('.py') and file != '__init__.py':
                    module_name = file[:-3]
                    module = import_module(
                        f'pymatpro.ansible.actions.{module_name}')
                    for cls_name in dir(module):
                        cls = getattr(module, cls_name)
                        if isinstance(cls, type) and cls.__name__.startswith('Mod'):
                            actions.append(cls)
        self.actions = {action.__name__[3:]: action for action in actions}

    def modify(self, modification, obj) -> None:
        if isinstance(obj, dict):
            self.modify_object(modification, obj)
        elif isinstance(obj, str) and os.path.exists(obj):
            with open(obj, 'r') as f:
                dct = json.load(f)
            self.modify_object(modification, dct)
            with open(obj, 'w') as f:
                json.dump(dct, f)
        else:
            raise ValueError("obj must be a dict or a valid filename")

    def modify_object(self, modification, obj):
        for action, value in modification.items():
            if action.startswith('_'):
                action = action[1:]
            if action in self.actions:
                self.actions[action](self, obj, value).operate()
            elif self.strict:
                raise ValueError(f"Invalid action: {action}")
