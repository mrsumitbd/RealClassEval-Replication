
import pathlib
from typing import Any, Dict, List, Union

import attr


# A very loose type alias for a colormap.  The actual type can be a
# dictionary mapping floats to RGBA tuples, a NumPy array, or any
# other representation that the user supplies.
ColorMapType = Any


@attr.s(frozen=True, slots=True)
class ColorMaps:
    """
    A registry for colormaps.  The registry is immutable; calling
    :meth:`register` returns a new instance with the updated mapping.
    """

    _cmap: Dict[str, ColorMapType] = attr.ib(
        default=attr.Factory(dict), init=False)

    def get(self, name: str) -> ColorMapType:
        """Return the colormap registered under *name*."""
        try:
            return self._cmap[name]
        except KeyError as exc:
            raise KeyError(f"Colormap '{name}' not found.") from exc

    def list(self) -> List[str]:
        """Return a sorted list of registered colormap names."""
        return sorted(self._cmap.keys())

    def register(
        self,
        custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]],
        overwrite: bool = False,
    ) -> "ColorMaps":
        """
        Register a custom colormap.

        Parameters
        ----------
        custom_cmap : dict
            Mapping of colormap names to colormap objects or file paths.
        overwrite : bool, optional
            If ``True`` an existing colormap with the same name will be
            replaced.  Defaults to ``False``.

        Returns
        -------
        ColorMaps
            A new instance with the updated registry.
        """
        new_cmap = dict(self._cmap)

        for name, cmap in custom_cmap.items():
            if not overwrite and name in new_cmap:
                raise ValueError(
                    f"Colormap '{name}' already exists. Use overwrite=True to replace it.")
            new_cmap[name] = cmap

        return attr.evolve(self, _cmap=new_cmap)
