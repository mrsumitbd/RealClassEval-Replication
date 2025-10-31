from domaintools.utils import convert_str_to_dateobj
from typing import List, Dict, Optional, Any, Callable

class filter_by_expire_date:
    """
    Returns the filtered result set by checking each result's expiration date.
    Can be before or after the given date.
    """

    def __init__(self, date: str, lookup_type='before'):
        self._date = date
        self._type = lookup_type

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results
        if self._date is None:
            return self._results
        if isinstance(self._date, str):
            self._date = convert_str_to_dateobj(self._date)
        filtered_result = []
        for result in self._results:
            domain_exp_date = result.get('expiration_date', {}).get('value') or None
            if not domain_exp_date:
                continue
            domain_exp_date = convert_str_to_dateobj(domain_exp_date)
            if self._type == 'before':
                if self._date < domain_exp_date:
                    filtered_result.append(result)
            elif self._type == 'after':
                if self._date > domain_exp_date:
                    filtered_result.append(result)
        return filtered_result