
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        self.base_cost_per_hour = 10.0  # Example base cost per hour

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        start_time = session_data.get('start_time', current_time)
        end_time = session_data.get('end_time', current_time)
        duration = end_time - start_time
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'duration_hours': duration.total_seconds() / 3600
        }

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        duration_hours = time_data.get('duration_hours', 0)
        predicted_cost = duration_hours * self.base_cost_per_hour
        within_limit = cost_limit is None or predicted_cost <= cost_limit
        return {
            'predicted_cost': predicted_cost,
            'within_cost_limit': within_limit
        }
