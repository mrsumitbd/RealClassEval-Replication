from typing import List, Dict, Optional, Any, Callable

class filter_by_riskscore:
    """Returns the filtered result set by a given risk score threshold."""

    def __init__(self, threshold: Optional[int]=None):
        self._threshold = threshold

    def __call__(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self._results = results
        if self._threshold is None:
            return self._results
        filtered_result = []
        for result in self._results:
            domain_risk_score = result.get('domain_risk', {}).get('risk_score')
            if domain_risk_score > self._threshold:
                filtered_result.append(result)
        return filtered_result