
from typing import Dict, Any, Optional
from datetime import datetime


class SessionCalculator:

    def __init__(self) -> None:
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time:
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds() / 3600  # in hours
        time_data['current_time'] = current_time
        return time_data

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        cost_predictions = {}
        rate = session_data.get('rate', 0)
        elapsed_time = time_data.get('elapsed_time', 0)
        cost_predictions['current_cost'] = rate * elapsed_time
        if cost_limit is not None:
            remaining_time = (
                cost_limit - cost_predictions['current_cost']) / rate
            cost_predictions['remaining_time'] = remaining_time if remaining_time > 0 else 0
        return cost_predictions
