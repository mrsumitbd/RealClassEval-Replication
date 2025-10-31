
import attr
import pathlib
from typing import Dict, List, Union, TypeVar

ColorMapType = TypeVar('ColorMapType')


@attr.s(frozen=True)
class ColorMaps:

    _cmaps: Dict[str, ColorMapType] = attr.ib(factory=dict)

    def get(self, name: str) -> ColorMapType:
        return self._cmaps[name]

    def list(self) -> List[str]:
        return list(self._cmaps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        new_cmaps = self._cmaps.copy()
        for key, value in custom_cmap.items():
            if key in new_cmaps and not overwrite:
                raise ValueError(
                    f"Colormap '{key}' already exists. Set overwrite=True to overwrite.")
            new_cmaps[key] = value
        return attr.evolve(self, _cmaps=new_cmaps)
