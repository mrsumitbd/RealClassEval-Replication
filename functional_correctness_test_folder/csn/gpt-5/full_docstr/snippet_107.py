import pathlib
from typing import Dict, List, Tuple, Union

import attr

try:
    from rio_tiler.colormap import DEFAULTS_CMAPS as _DEFAULTS_CMAPS  # type: ignore
except Exception:  # pragma: no cover
    _DEFAULTS_CMAPS = {}

try:
    import numpy as _np  # type: ignore
except Exception:  # pragma: no cover
    _np = None  # numpy is optional for loading .npy colormaps


ColorMapType = Dict[int, Tuple[int, int, int, int]]


def _default_data_factory() -> Dict[str, ColorMapType]:
    return dict(_DEFAULTS_CMAPS)


def _ensure_rgba_dict(arr) -> ColorMapType:
    if _np is None:
        raise RuntimeError(
            "numpy is required to load colormap from .npy files")
    a = _np.asarray(arr)
    if a.ndim != 2 or a.shape[0] == 0:
        raise ValueError("Invalid colormap array")
    if a.shape[1] not in (3, 4):
        raise ValueError(
            "Colormap array must have 3 (RGB) or 4 (RGBA) columns")
    if a.dtype != _np.uint8:
        a = a.astype(_np.uint8)
    if a.shape[1] == 3:
        alpha = _np.full((a.shape[0], 1), 255, dtype=_np.uint8)
        a = _np.concatenate([a, alpha], axis=1)
    return {int(i): (int(r), int(g), int(b), int(aa)) for i, (r, g, b, aa) in enumerate(a)}


def _load_cmap_from_path(path: Union[str, pathlib.Path]) -> ColorMapType:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Colormap file not found: {p}")
    if p.suffix.lower() == ".npy":
        if _np is None:
            raise RuntimeError("numpy is required to load .npy colormap files")
        arr = _np.load(str(p))
        return _ensure_rgba_dict(arr)
    raise ValueError(f"Unsupported colormap file type: {p.suffix}")


@attr.s(frozen=True)
class ColorMaps:
    '''Default Colormaps holder.
    Attributes:
        data (dict): colormaps. Defaults to `rio_tiler.colormap.DEFAULTS_CMAPS`.
    '''
    data: Dict[str, ColorMapType] = attr.ib(factory=_default_data_factory)

    def get(self, name: str) -> ColorMapType:
        '''Fetch a colormap.
        Args:
            name (str): colormap name.
        Returns
            dict: colormap dictionary.
        '''
        try:
            return self.data[name]
        except KeyError as exc:
            raise KeyError(f"Colormap '{name}' not found") from exc

    def list(self) -> List[str]:
        '''List registered Colormaps.
        Returns
            list: list of colormap names.
        '''
        return sorted(self.data.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        '''Register a custom colormap.
        Args:
            custom_cmap (dict): custom colormap(s) to register.
            overwrite (bool): Overwrite existing colormap with same key. Defaults to False.
        Examples:
            >>> cmap = cmap.register({"acmap": {0: (0, 0, 0, 0), ...}})
            >>> cmap = cmap.register({"acmap": "acmap.npy"})
        '''
        if not isinstance(custom_cmap, dict):
            raise TypeError("custom_cmap must be a dict of name -> colormap")
        new_data = dict(self.data)
        for name, value in custom_cmap.items():
            if not overwrite and name in new_data:
                raise ValueError(
                    f"Colormap '{name}' already exists. Use overwrite=True to replace.")
            if isinstance(value, (str, pathlib.Path)):
                cmap_dict = _load_cmap_from_path(value)
            elif isinstance(value, dict):
                # Ensure entries are RGBA tuples with 4 components
                cmap_dict = {}
                for k, v in value.items():
                    if not isinstance(k, int):
                        try:
                            k = int(k)  # allow string-int keys
                        except Exception as exc:
                            raise TypeError(
                                "Colormap keys must be integers") from exc
                    if isinstance(v, tuple):
                        t = v
                    elif isinstance(v, list):
                        t = tuple(v)
                    else:
                        raise TypeError(
                            "Colormap values must be tuples or lists of 3 or 4 integers")
                    if len(t) == 3:
                        t = (t[0], t[1], t[2], 255)
                    if len(t) != 4:
                        raise ValueError(
                            "Colormap values must have length 3 (RGB) or 4 (RGBA)")
                    r, g, b, a = t
                    cmap_dict[k] = (int(r), int(g), int(b), int(a))
            else:
                raise TypeError(
                    "Colormap value must be a dict, path string, or pathlib.Path")
            new_data[name] = cmap_dict
        return attr.evolve(self, data=new_data)
