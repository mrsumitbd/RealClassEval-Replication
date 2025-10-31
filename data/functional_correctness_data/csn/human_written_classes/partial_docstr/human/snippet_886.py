from typing import List, Dict, Optional, Any, Callable

class DTResultFilter:
    """Calls the given available callable filters."""

    def __init__(self, result_set, item_path: Optional[str]='results'):
        self._result_set = result_set.get(item_path) or []

    def by(self, available_filters: List[Callable]):
        for _dt_filter in available_filters:
            self._result_set = _dt_filter(self._result_set)
        return self._result_set