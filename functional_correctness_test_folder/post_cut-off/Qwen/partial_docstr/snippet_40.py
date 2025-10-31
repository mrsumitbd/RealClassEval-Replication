
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        start_time = session_data.get('start_time', current_time)
        end_time = session_data.get('end_time', current_time)
        duration = end_time - start_time
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration.total_seconds() / 3600  # Duration in hours
        }

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        '''Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        '''
        if cost_limit is None:
            cost_limit = 100.0

        hourly_rate = session_data.get('hourly_rate', 0.0)
        duration_hours = time_data.get('duration', 0.0)
        predicted_cost = hourly_rate * duration_hours

        return {
            'predicted_cost': predicted_cost,
            'within_cost_limit': predicted_cost <= cost_limit
        }
