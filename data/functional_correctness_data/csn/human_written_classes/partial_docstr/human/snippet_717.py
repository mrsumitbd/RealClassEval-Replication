from mapchete.bounds import Bounds
from typing import Any, Dict, Iterable, List, Literal, Optional, Tuple, Union
from mapchete.types import BoundsLike, CRSLike, MPathLike, GeoJSONLikeFeature, Geometry

class FakeIndex:
    """Provides a fake spatial index in case rtree is not installed."""
    _items: List[Tuple[int, Bounds]]

    def __init__(self):
        self._items = []

    def insert(self, id: int, bounds: BoundsLike):
        self._items.append((id, Bounds.from_inp(bounds)))

    def intersection(self, bounds: BoundsLike) -> List[int]:
        return [id for id, i_bounds in self._items if Bounds.from_inp(i_bounds).intersects(bounds)]