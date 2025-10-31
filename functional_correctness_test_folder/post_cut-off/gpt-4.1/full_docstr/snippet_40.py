
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


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
        start_time = session_data.get('start_time')
        end_time = session_data.get('end_time')
        duration = None
        elapsed = None
        remaining = None
        is_active = False

        if start_time and isinstance(start_time, datetime):
            if end_time and isinstance(end_time, datetime):
                duration = end_time - start_time
                elapsed = min(current_time, end_time) - start_time
                remaining = max(timedelta(0), end_time - current_time)
                is_active = start_time <= current_time < end_time
            else:
                elapsed = current_time - start_time
                duration = None
                remaining = None
                is_active = current_time >= start_time

        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'elapsed': elapsed,
            'remaining': remaining,
            'is_active': is_active
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
        elapsed = time_data.get('elapsed')
        duration = time_data.get('duration')

        elapsed_hours = elapsed.total_seconds() / 3600 if elapsed else 0.0
        duration_hours = duration.total_seconds() / 3600 if duration else None

        current_cost = elapsed_hours * cost_per_hour
        predicted_total_cost = None
        time_to_limit = None

        if duration_hours is not None:
            predicted_total_cost = duration_hours * cost_per_hour
        else:
            predicted_total_cost = None

        if cost_per_hour > 0:
            remaining_cost = cost_limit - current_cost
            if remaining_cost > 0:
                time_to_limit = timedelta(hours=remaining_cost / cost_per_hour)
            else:
                time_to_limit = timedelta(0)
        else:
            time_to_limit = None

        return {
            'cost_per_hour': cost_per_hour,
            'current_cost': current_cost,
            'predicted_total_cost': predicted_total_cost,
            'cost_limit': cost_limit,
            'time_to_limit': time_to_limit
        }
