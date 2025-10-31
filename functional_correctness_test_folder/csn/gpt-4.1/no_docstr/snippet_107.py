
import attr
import pathlib
from typing import Dict, Union, List, Any

# You can replace Any with Tuple[int, int, int, int] if needed
ColorMapType = Dict[int, Any]


@attr.s(frozen=True)
class ColorMaps:
    _colormaps: Dict[str, ColorMapType] = attr.ib(factory=dict)

    def get(self, name: str) -> ColorMapType:
        if name not in self._colormaps:
            raise KeyError(f"Colormap '{name}' not found.")
        return self._colormaps[name]

    def list(self) -> List[str]:
        return list(self._colormaps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        new_colormaps = dict(self._colormaps)
        for key, value in custom_cmap.items():
            if not overwrite and key in new_colormaps:
                raise ValueError(
                    f"Colormap '{key}' already exists. Use overwrite=True to replace it.")
            if isinstance(value, (str, pathlib.Path)):
                # Assume it's a path to a .npy file
                import numpy as np
                arr = np.load(str(value), allow_pickle=True)
                if isinstance(arr, dict):
                    cmap = dict(arr)
                else:
                    # Assume arr is a Nx4 array, map index to tuple
                    cmap = {i: tuple(arr[i]) for i in range(arr.shape[0])}
                new_colormaps[key] = cmap
            elif isinstance(value, dict):
                new_colormaps[key] = dict(value)
            else:
                raise TypeError(
                    f"Unsupported colormap type for '{key}': {type(value)}")
        return ColorMaps(new_colormaps)
