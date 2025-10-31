import pathlib
from typing import Dict, Union, List, Tuple, Any
import numpy as np
import attr

ColorMapType = Union[np.ndarray, Dict[int, Tuple[float, float,
                                                 float, float]], List[Tuple[float, float, float, float]]]


def _to_array(cmap: ColorMapType) -> np.ndarray:
    if isinstance(cmap, np.ndarray):
        arr = np.array(cmap, dtype=float)
    elif isinstance(cmap, dict):
        if not cmap:
            raise ValueError("Colormap dict cannot be empty.")
        # Sort by numeric keys
        try:
            items = sorted(cmap.items(), key=lambda kv: float(kv[0]))
        except Exception as e:
            raise ValueError(
                f"Invalid colormap dict keys; must be numeric-sortable. {e}")
        arr = np.array([kv[1] for kv in items], dtype=float)
    else:
        # Assume list-like of tuples
        arr = np.array(cmap, dtype=float)

    if arr.ndim != 2 or arr.shape[1] not in (3, 4):
        raise ValueError("Colormap array must be of shape (N, 3) or (N, 4).")
    if arr.shape[1] == 3:
        alpha = np.ones((arr.shape[0], 1), dtype=float)
        arr = np.concatenate([arr, alpha], axis=1)
    # Clip to [0,1]
    arr = np.clip(arr, 0.0, 1.0)
    return arr


def _load_from_path(p: Union[str, pathlib.Path]) -> np.ndarray:
    path = pathlib.Path(p)
    if not path.exists():
        raise FileNotFoundError(f"Colormap file not found: {path}")
    if path.suffix.lower() == ".npy":
        data = np.load(str(path), allow_pickle=True)
        # If saved dict or array
        if isinstance(data, np.ndarray) and data.dtype == object:
            # Try to unwrap single object (common when saving dict with np.save)
            if data.shape == ():
                data = data.item()
        return _to_array(data)
    elif path.suffix.lower() == ".npz":
        data = np.load(str(path), allow_pickle=True)
        # Try common keys
        for key in ("cmap", "colormap", "arr", "data"):
            if key in data:
                return _to_array(data[key])
        # Fallback: first array
        if len(list(data.files)) > 0:
            return _to_array(data[data.files[0]])
        raise ValueError(f"No array-like data found in {path}")
    else:
        raise ValueError(f"Unsupported colormap file extension: {path.suffix}")


@attr.s(frozen=True)
class ColorMaps:
    _maps: Dict[str, np.ndarray] = attr.ib(factory=dict)

    def get(self, name: str) -> ColorMapType:
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")
        try:
            arr = self._maps[name]
        except KeyError:
            raise KeyError(f"Colormap '{name}' is not registered.")
        return np.array(arr, copy=True)

    def list(self) -> List[str]:
        return sorted(self._maps.keys())

    def register(self, custom_cmap: Dict[str, Union[str, pathlib.Path, ColorMapType]], overwrite: bool = False) -> 'ColorMaps':
        if not isinstance(custom_cmap, dict) or not custom_cmap:
            raise ValueError(
                "custom_cmap must be a non-empty dict of name -> colormap.")
        new_maps = dict(self._maps)
        for name, spec in custom_cmap.items():
            if not isinstance(name, str) or not name:
                raise ValueError(
                    "All colormap names must be non-empty strings.")
            if (not overwrite) and (name in new_maps):
                raise KeyError(
                    f"Colormap '{name}' already exists. Use overwrite=True to replace it.")
            if isinstance(spec, (str, pathlib.Path)):
                arr = _load_from_path(spec)
            else:
                arr = _to_array(spec)
            new_maps[name] = arr
        return attr.evolve(self, _maps=new_maps)
