
from typing import Dict, Any, Optional
from datetime import datetime


class SessionCalculator:

    def __init__(self) -> None:
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        time_data = {}
        if 'start_time' in session_data:
            start_time = session_data['start_time']
            elapsed_time = (current_time - start_time).total_seconds()
            time_data['elapsed_time'] = elapsed_time
        return time_data

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        cost_predictions = {}
        if 'elapsed_time' in time_data and 'cost_rate' in session_data:
            elapsed_time = time_data['elapsed_time']
            cost_rate = session_data['cost_rate']
            current_cost = elapsed_time * cost_rate
            cost_predictions['current_cost'] = current_cost

            if cost_limit is not None:
                remaining_budget = max(0.0, cost_limit - current_cost)
                cost_predictions['remaining_budget'] = remaining_budget

                if cost_rate > 0:
                    remaining_time = remaining_budget / cost_rate
                    cost_predictions['remaining_time'] = remaining_time
        return cost_predictions
