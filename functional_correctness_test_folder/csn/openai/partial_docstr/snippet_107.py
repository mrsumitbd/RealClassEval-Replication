
import pathlib
from typing import Dict, List, Union, Tuple

import attr
import numpy as np

from rio_tiler.colormap import DEFAULTS_CMAPS, ColorMapType


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(default=DEFAULTS_CMAPS)

    def get(self, name: str) -> ColorMapType:
        """Return the colormap for the given name."""
        try:
            return self.data[name]
        except KeyError as exc:
            raise KeyError(f"Colormap '{name}' not found.") from exc

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return sorted(self.data.keys())

    def register(
        self,
        custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]],
        overwrite: bool = False,
    ) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        new_data = dict(self.data)

        for key, value in custom_cmap.items():
            if isinstance(value, (str, pathlib.Path)):
                path = pathlib.Path(value)
                if not path.is_file():
                    raise FileNotFoundError(
                        f"Colormap file '{path}' does not exist.")
                try:
                    arr = np.load(path)
                except Exception as exc:
                    raise ValueError(
                        f"Failed to load colormap from '{path}': {exc}") from exc
                if arr.ndim != 2 or arr.shape[1] != 4:
                    raise ValueError(
                        f"Colormap file '{path}' must contain an array of shape (n, 4)."
                    )
                cmap_dict = {int(idx): tuple(map(int, row))
                             for idx, row in enumerate(arr)}
                cmap_value = cmap_dict
            elif isinstance(value, dict):
                cmap_value = value
            else:
                raise TypeError(
                    f"Unsupported colormap type for key '{key}': {type(value).__name__}"
                )

            if not overwrite and key in new_data:
                raise ValueError(
                    f"Colormap '{key}' already exists. Use overwrite=True to replace.")
            new_data[key] = cmap_value

        return attr.evolve(self, data=new_data)
