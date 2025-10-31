from typing import Callable, Any, TypeVar, Dict, Union, List, Optional, Tuple, Set
from fletx.core.state import Reactive, ReactiveDependencyTracker, Computed, Observer

class ReactiveMemoryCache:
    """Cache for memoized reactive computations"""

    def __init__(self, maxsize: int=128):
        self.maxsize = maxsize
        self.cache: Dict[str, Tuple[Any, Set[Reactive]]] = {}
        self.access_order: List[str] = []

    def get(self, key: str) -> Optional[Tuple[Any, Set[Reactive]]]:
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: Any, dependencies: Set[Reactive]):
        if len(self.cache) >= self.maxsize and key not in self.cache:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        self.cache[key] = (value, dependencies)
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)

    def invalidate(self, key: str):
        if key in self.cache:
            del self.cache[key]
            self.access_order.remove(key)