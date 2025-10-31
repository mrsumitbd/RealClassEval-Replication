
import json
import os
from typing import Any, Dict, List, Optional, Type


class _BaseAction:
    """Base class for all actions."""

    keyword: str = ""

    def apply(self, value: Any, obj: Any) -> None:
        """Apply the action to the object."""
        raise NotImplementedError


class _SetAction(_BaseAction):
    keyword = "_set"

    def apply(self, value: Dict[str, Any], obj: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise ValueError(
                f"{self.keyword} expects a dict, got {type(value)}")
        for k, v in value.items():
            obj[k] = v


class _UnsetAction(_BaseAction):
    keyword = "_unset"

    def apply(self, value: List[str], obj: Dict[str, Any]) -> None:
        if not isinstance(value, list):
            raise ValueError(
                f"{self.keyword} expects a list, got {type(value)}")
        for k in value:
            obj.pop(k, None)


class Modder:
    """
    Class to modify a dict/file/any object using a mongo-like language.
    Keywords are mostly adopted from mongo's syntax, but instead of `$`, an
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
    """

    def __init__(
        self,
        actions: Optional[List[Type[_BaseAction]]] = None,
        strict: bool = True,
        directory: str = "./",
    ) -> None:
        """
        Parameters
        ----------
        actions : list of action classes
            List of classes that implement the action logic. If None, a
            default set of actions is used.
        strict : bool
            If True, unknown actions raise an error. If False, they are ignored.
        directory : str
            Base directory for file operations (not used in this minimal
            implementation).
        """
        self.strict = strict
        self.directory = directory

        # Default actions if none provided
        if actions is None:
            actions = [_SetAction, _UnsetAction]

        # Instantiate actions and map keyword to instance
        self.action_map: Dict[str, _BaseAction] = {}
        for act_cls in actions:
            if not issubclass(act_cls, _BaseAction):
                raise TypeError(f"Action {act_cls} must subclass _BaseAction")
            act = act_cls()
            if act.keyword in self.action_map:
                raise ValueError(f"Duplicate action keyword: {act.keyword}")
            self.action_map[act.keyword] = act

    def modify(self, modification: Any, obj: Any) -> None:
        """
        Apply a modification to an object.

        Parameters
        ----------
        modification : dict or list
            The modification specification.
        obj : dict or file path
            The object to modify. If a string, it is treated as a file path
            and the file is loaded as JSON, modified, and written back.
        """
        if isinstance(obj, str):
            # Treat as file path
            path = os.path.join(self.directory, obj)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.modify_object(modification, data)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        elif isinstance(obj, dict):
            self.modify_object(modification, obj)
        else:
            raise TypeError(f"Unsupported object type: {type(obj)}")

    def modify_object(self, modification: Any, obj: Any) -> None:
        """
        Recursively apply modifications to a dict-like object.

        Parameters
        ----------
        modification : dict
            The modification specification.
        obj : dict
            The target dictionary to modify.
        """
        if not isinstance(modification, dict):
            raise ValueError("Modification must be a dict")

        for key, value in modification.items():
            if key.startswith("_"):
                # Action keyword
                action = self.action_map.get(key)
                if action is None:
                    if self.strict:
                        raise KeyError(f"Unknown action keyword: {key}")
                    else:
                        continue
                action.apply(value, obj)
            else:
                # Nested modification
                if key not in obj or not isinstance(obj[key], dict):
                    # Create nested dict if missing or not a dict
                    obj[key] = {}
                if isinstance(value, dict):
                    self.modify_object(value, obj[key])
                else:
                    # Direct assignment for non-dict values
                    obj[key] = value
