from typing import Any, Dict, Iterable, Optional, cast, Union, SupportsInt, Tuple

class MissingValueSpec:
    """ Stores the information about how to find and treat missing
        values.

        :ivar str sentinel: sentinel is the string that identifies a
            missing value e.g.: 'N/A', ''.
            The sentinel will not be validated against the
            feature format definition
        :ivar str replace_with: defines the string which replaces the
            sentinel whenever present, can be 'None', then sentinel will
            not be replaced.

    """

    def __init__(self, sentinel: str, replace_with: Optional[str]=None) -> None:
        self.sentinel = sentinel
        self.replace_with = replace_with if replace_with is not None else sentinel

    @classmethod
    def from_json_dict(cls, json_dict: Dict[str, Any]) -> 'MissingValueSpec':
        return cls(sentinel=json_dict['sentinel'], replace_with=cast(Optional[str], json_dict.get('replaceWith')))