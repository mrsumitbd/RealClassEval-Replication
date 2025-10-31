from dataclasses import dataclass, field
import numpy as np
from typing import Any, Union

@dataclass
class Realization:
    """
    Represents a realization of a node in a logic tree.

    Parameters
    ----------
    name : str
        The name of the realization.
    value : Union[str, float, int]
        The value of the realization.
    weight : float, optional
        The weight of the realization, by default 1.
    params : Dict[str, Any], optional
        Additional parameters for the realization, by default an empty dict.
    requires : Dict[str, Any], optional
        Requirements for this realization to be valid, by default an empty dict.
    excludes : Dict[str, Any], optional
        Exclusions for this realization to be valid, by default an empty dict.
    """
    name: str
    value: str | float | int
    weight: float = 1
    params: dict[str, Any] = field(default_factory=dict)
    requires: dict[str, Any] = field(default_factory=dict)
    excludes: dict[str, Any] = field(default_factory=dict)

    def is_valid(self, branch):
        """
        Check if this realization is valid given a branch.

        Parameters
        ----------
        branch : Branch
            The branch to check against.

        Returns
        -------
        bool
            True if the realization is valid, False otherwise.
        """

        def matches(ref, check):
            if isinstance(ref, list):
                ret = check in ref
            elif isinstance(ref, float):
                ret = np.isclose(ref, check)
            else:
                ret = ref == check
            return ret
        okay = True
        if self.requires:
            okay = all((matches(v, branch[k].value) for k, v in self.requires.items()))
        if okay and self.excludes:
            okay &= not all((matches(v, branch[k].value) for k, v in self.excludes.items()))
        return okay