
from typing import Dict, Union, List
import attr
import pathlib

ColorMapType = Dict[int, tuple]


@attr.s(frozen=True)
class ColorMaps:
    _colormaps = attr.ib(init=False, default=attr.Factory(dict))

    def get(self, name: str) -> ColorMapType:
        return self._colormaps[name]

    def list(self) -> List[str]:
        return list(self._colormaps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        new_colormaps = self._colormaps.copy()
        for name, cmap in custom_cmap.items():
            if name in new_colormaps and not overwrite:
                raise ValueError(
                    f"Colormap '{name}' already exists. Set overwrite=True to replace it.")
            if isinstance(cmap, (str, pathlib.Path)):
                # Here you would typically load the colormap from the file
                # For the sake of this example, we'll just store the path
                new_colormaps[name] = cmap
            else:
                new_colormaps[name] = cmap
        return ColorMaps._make(new_colormaps)

    @classmethod
    def _make(cls, colormaps: Dict[str, Union[str, pathlib.Path, ColorMapType]]) -> 'ColorMaps':
        instance = cls()
        object.__setattr__(instance, '_colormaps', colormaps)
        return instance
