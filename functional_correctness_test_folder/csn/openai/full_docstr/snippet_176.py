
import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Type

# --------------------------------------------------------------------------- #
# Minimal action infrastructure
# --------------------------------------------------------------------------- #


class BaseAction:
    """Base class for all actions."""
    keyword: str = ""

    def modify(self, settings: Any, obj: Any) -> None:
        """Apply the action to the object."""
        raise NotImplementedError


class SetAction(BaseAction):
    """Implements the '_set' action for dictionaries."""
    keyword = "_set"

    def modify(self, settings: Dict[str, Any], obj: Dict[str, Any]) -> None:
        for key, value in settings.items():
            obj[key] = value


# --------------------------------------------------------------------------- #
# Modder implementation
# --------------------------------------------------------------------------- #
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
        actions: Optional[Sequence[Type[BaseAction]]] = None,
        strict: bool = True,
        directory: str = "./",
    ) -> None:
        """
        Initialize a Modder from a list of supported actions.
        Args:
            actions ([Action]): A sequence of supported actions. See
                :mod:`custodian.ansible.actions`. Default is None,
                which means only DictActions are supported.
            strict (bool): Indicating whether to use strict mode. In
                non-strict mode, unsupported actions are simply ignored
                without any errors raised. In strict mode, if an
                unsupported action is supplied, a ValueError is raised.
                Defaults to True.
            directory (str): The directory containing the files to be
                modified. Defaults to "./".
        """
        if actions is None:
            actions = [SetAction]
        self.actions: List[Type[BaseAction]] = list(actions)
        self.strict: bool = strict
        self.directory: str = directory

    # ----------------------------------------------------------------------- #
    # Public API
    # ----------------------------------------------------------------------- #
    def modify(self, modification: Dict[str, Any], obj: Any) -> None:
        """
        Note that modify makes actual in-place modifications. It does not
        return a copy.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (dict/str/object): Object to modify depending on actions.
                For example, for DictActions, obj will be a dict to be
                modified. For FileActions, obj will be a string with a
                full pathname to a file.
        """
        if isinstance(obj, dict):
            self._modify_dict(modification, obj)
        elif isinstance(obj, str) and os.path.isfile(os.path.join(self.directory, obj)):
            self._modify_file(modification, obj)
        elif hasattr(obj, "as_dict") and hasattr(obj.__class__, "from_dict"):
            self.modify_object(modification, obj)
        else:
            raise TypeError(
                f"Unsupported object type for modification: {type(obj).__name__}"
            )

    def modify_object(self, modification: Dict[str, Any], obj: Any) -> None:
        """
        Modify an object that supports pymatgen's as_dict() and from_dict API.
        Args:
            modification (dict): Modification must be {action_keyword :
                settings}. E.g., {'_set': {'Hello':'Universe', 'Bye': 'World'}}
            obj (object): Object to modify
        """
        obj_dict = obj.as_dict()
        self._modify_dict(modification, obj_dict)
        # Reconstruct the object and update the original instance
        new_obj = obj.__class__.from_dict(obj_dict)
        obj.__dict__.update(new_obj.__dict__)

    # ----------------------------------------------------------------------- #
    # Internal helpers
    # ----------------------------------------------------------------------- #
    def _modify_dict(self, modification: Dict[str, Any], obj: Dict[str, Any]) -> None:
        for action_keyword, settings in modification.items():
            action_cls = self._find_action(action_keyword)
            if action_cls is None:
                if self.strict:
                    raise ValueError(f"Unsupported action: {action_keyword}")
                continue
            action = action_cls()
            action.modify(settings, obj)

    def _modify_file(self, modification: Dict[str, Any], file_path: str) -> None:
        """
        Very minimal file modification support: only supports '_set' by
        writing key=value pairs into the file (one per line). This is a
        placeholder implementation.
        """
        full_path = os.path.join(self.directory, file_path)
        if "_set" not in modification:
            if self.strict:
                raise ValueError("Only '_set' action is supported for files.")
            return
        lines = []
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-
