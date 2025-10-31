from typing import List, Dict, Optional, Any, Callable
from domaintools.utils import convert_str_to_dateobj

class filter_by_date_updated_after:
    """Returns the filtered result set by checking each result's 'date_updated_after' field."""

    def __init__(self, date: str):
        self._updated_after_date = date

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results
        if self._updated_after_date is None:
            return self._results
        if isinstance(self._updated_after_date, str):
            self._updated_after_date = convert_str_to_dateobj(self._updated_after_date)
        filtered_result = []
        for result in self._results:
            data_updated_timestamp = result.get('data_updated_timestamp') or None
            if not data_updated_timestamp:
                continue
            data_updated_timestamp = convert_str_to_dateobj(data_updated_timestamp, date_format='%Y-%m-%dT%H:%M:%S.%f')
            if data_updated_timestamp > self._updated_after_date:
                filtered_result.append(result)
        return filtered_result