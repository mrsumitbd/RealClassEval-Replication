from typing import List, Dict, Optional, Any, Callable

class filter_by_field:
    """
    Returns the filtered result by checking if the field exits on each results.
    Can be included or excluded based on the `filter_type` param given.
    """

    def __init__(self, field: str, filter_type: str='include'):
        self._field = field
        self._filter_type = filter_type

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results
        if self._field is None:
            return self._results
        filtered_result = []
        for result in self._results:
            result_keys = result.keys()
            lookup_field = result.get(self._field) or None
            if self._filter_type == 'include':
                if not lookup_field or lookup_field:
                    filtered_result.append(result)
                continue
            elif self._filter_type == 'exclude':
                if lookup_field:
                    filtered_result.append(result)
        return filtered_result