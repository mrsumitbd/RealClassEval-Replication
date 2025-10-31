
import attr
from typing import List, Dict, Union
import pathlib
import numpy as np
from matplotlib.colors import ListedColormap
from copy import deepcopy

ColorMapType = ListedColormap


@attr.s(frozen=True)
class ColorMaps:
    _cmaps = attr.ib(factory=dict)

    def get(self, name: str) -> ColorMapType:
        return self._cmaps[name]

    def list(self) -> List[str]:
        return list(self._cmaps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType, Dict]], overwrite: bool = False) -> 'ColorMaps':
        new_cmaps = deepcopy(self._cmaps)
        for name, cmap in custom_cmap.items():
            if isinstance(cmap, (str, pathlib.Path)):
                cmap = np.load(cmap)
                cmap = ListedColormap(cmap)
            elif isinstance(cmap, dict):
                cmap = ListedColormap(cmap)
            if name in new_cmaps and not overwrite:
                raise ValueError(
                    f"Colormap {name} already exists. Use overwrite=True to overwrite.")
            new_cmaps[name] = cmap
        return attr.evolve(self, cmaps=new_cmaps)
