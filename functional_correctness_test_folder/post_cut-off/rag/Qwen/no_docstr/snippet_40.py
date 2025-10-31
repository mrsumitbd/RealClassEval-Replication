
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        '''
        start_time = session_data.get('start_time', current_time)
        end_time = session_data.get('end_time', current_time)
        duration = end_time - start_time
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'is_active': end_time > current_time
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

        cost_per_hour = session_data.get('cost_per_hour', 0.0)
        duration = time_data.get('duration', timedelta())
        total_cost = (duration.total_seconds() / 3600) * cost_per_hour
        remaining_cost = cost_limit - total_cost
        is_within_limit = remaining_cost >= 0

        return {
            'cost_per_hour': cost_per_hour,
            'total_cost': total_cost,
            'remaining_cost': remaining_cost,
            'is_within_limit': is_within_limit
        }
