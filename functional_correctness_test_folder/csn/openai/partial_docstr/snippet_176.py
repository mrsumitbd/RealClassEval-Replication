
import json
import os
import inspect
from typing import Any, Dict, List, Optional, Type

# Import all action classes from pymatpro.ansible.actions if available
try:
    from pymatpro.ansible import actions as _actions_module
    _action_classes = [
        cls for _, cls in inspect.getmembers(_actions_module, inspect.isclass)
        if hasattr(cls, "keyword")
    ]
except Exception:
    # If the module is not available, fall back to an empty list
    _action_classes = []


class Modder:
    """
    Class to modify a dict/file/any object using a mongo-like language.
    Keywords are mostly adopted from mongo's syntax, but instead of `$`,
    an underscore precedes action keywords. This is so that the modification
    can be inserted into a mongo db easily.
    Allowable actions are supplied as a list of classes as an argument.
    Refer to the action classes on what the actions do. Action classes are
    in pymatpro.ansible.actions.
    Examples:
    >>> modder = Modder()
    >>> dct = {"Hello": "World"}
    >>> mod = {'_set': {'Hello':'Universe', 'Bye': 'World'}}
    >>> modder.modify(mod, dct)
    >>> dct['Bye']
    'World'
    >>> dct['Hello']
    'Universe'
    """

    def __init__(
        self,
        actions: Optional[List[Type]] = None,
        strict: bool = True,
        directory: str = "./",
    ) -> None:
        """
        Parameters
        ----------
        actions : list of classes, optional
            List of action classes that implement a `keyword` attribute
            and a `modify` method. If None, defaults to the actions
            discovered from pymatpro.ansible.actions.
        strict : bool, optional
            If True, raise an error when an unknown action keyword is
            encountered. If False, silently ignore unknown keywords.
        directory : str, optional
            Base directory for relative file paths.
        """
        if actions is None:
            actions = _action_classes
        self._action_map: Dict[str, Type] = {}
        for act_cls in actions:
            kw = getattr(act_cls, "keyword", None)
            if kw:
                self._action_map[kw] = act_cls
        self.strict = strict
        self.directory = os.path.abspath(directory)

    def modify(self, modification: Dict[str, Any], obj: Any) -> None:
        """
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Parameters
        ----------
        modification : dict
            Modification must be {action_keyword : settings}. E.g.,
            {'_set': {'Hello':'Universe', 'Bye': 'World'}}
        obj : object
            Object to modify. Can be a dict, a file path (JSON), or an
            object that implements as_dict() and from_dict().
        """
        if isinstance(obj, dict):
            self._modify_dict(modification, obj)
        elif isinstance(obj, str) and os.path.isfile(os.path.join(self.directory, obj)):
            self._modify_file(modification, obj)
        elif hasattr(obj, "as_dict") and hasattr(obj, "from_dict"):
            self.modify_object(modification, obj)
        else:
            raise TypeError(
                f"Unsupported object type for modification: {type(obj).__name__}"
            )

    def _modify_dict(self, modification: Dict[str, Any], dct: Dict[str, Any]) -> None:
        for key, settings in modification.items():
            act_cls = self._action_map.get(key)
            if act_cls is None:
                if self.strict:
                    raise ValueError(f"Unknown action keyword: {key}")
                continue
            action = act_cls(settings)
            action.modify(dct)

    def _modify_file(self, modification: Dict[str, Any], file_path: str) -> None:
        full_path = os.path.join(self.directory, file_path)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("JSON file must contain a top-level object")
        self._modify_dict(modification, data)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def modify_object(self, modification: Dict[str, Any], obj: Any) -> None:
        """
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Parameters
        ----------
        modification : dict
            Modification must be {action_keyword : settings}. E.g.,
            {'_set': {'Hello':'Universe', 'Bye': 'World'}}
        obj : object
            Object to modify
        """
        dct = obj.as_dict()
        self._modify_dict(modification, dct)
        # Update the object's attributes in place
        for key, value in dct.items():
            setattr(obj, key, value)
