
import pathlib
from typing import Dict, List, Union
import attr
import numpy as np
from matplotlib.colors import ListedColormap

ColorMapType = ListedColormap


@attr.s(frozen=True)
class ColorMaps:
    _cmaps: Dict[str, ColorMapType] = attr.ib(factory=dict, init=False)

    def get(self, name: str) -> ColorMapType:
        if name not in self._cmaps:
            raise ValueError(f"Colormap '{name}' not found.")
        return self._cmaps[name]

    def list(self) -> List[str]:
        return list(self._cmaps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        new_cmaps = self._cmaps.copy()
        for name, cmap_data in custom_cmap.items():
            if not overwrite and name in new_cmaps:
                raise ValueError(
                    f"Colormap '{name}' already exists and overwrite is False.")

            if isinstance(cmap_data, (str, pathlib.Path)):
                cmap_array = np.load(str(cmap_data))
                cmap = ListedColormap(cmap_array)
            elif isinstance(cmap_data, ColorMapType):
                cmap = cmap_data
            elif isinstance(cmap_data, dict):
                colors = [cmap_data[key] for key in sorted(cmap_data.keys())]
                cmap = ListedColormap(colors)
            else:
                raise ValueError(
                    f"Unsupported colormap data type for '{name}'.")

            new_cmaps[name] = cmap

        return ColorMaps(**{'_cmaps': new_cmaps})
