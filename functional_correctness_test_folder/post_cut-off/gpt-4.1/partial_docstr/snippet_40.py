
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''
        Calculates time-related data for a session.
        Args:
            session_data: Dictionary containing session start time and duration info.
            current_time: The current datetime.
        Returns:
            Dictionary with time data.
        '''
        start_time = session_data.get(
            'start_time')  # expected to be a datetime
        # expected to be a timedelta or float (hours)
        duration = session_data.get('duration')
        if isinstance(duration, (int, float)):
            duration = timedelta(hours=duration)
        elif not isinstance(duration, timedelta):
            duration = timedelta(0)
        elapsed = current_time - start_time if start_time else timedelta(0)
        remaining = duration - elapsed if duration > elapsed else timedelta(0)
        is_active = elapsed < duration
        return {
            'start_time': start_time,
            'duration': duration,
            'elapsed': elapsed,
            'remaining': remaining,
            'is_active': is_active,
            'end_time': start_time + duration if start_time else None
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
        duration = time_data.get('duration', timedelta(0))
        elapsed = time_data.get('elapsed', timedelta(0))
        remaining = time_data.get('remaining', timedelta(0))
        total_hours = duration.total_seconds() / 3600
        elapsed_hours = elapsed.total_seconds() / 3600
        remaining_hours = remaining.total_seconds() / 3600
        total_cost = cost_per_hour * total_hours
        cost_so_far = cost_per_hour * elapsed_hours
        cost_remaining = cost_per_hour * remaining_hours
        if cost_per_hour > 0:
            hours_until_limit = cost_limit / cost_per_hour
            time_until_limit = timedelta(hours=hours_until_limit)
            if elapsed < time_until_limit:
                limit_reached_at = time_data['start_time'] + \
                    time_until_limit if time_data['start_time'] else None
            else:
                limit_reached_at = time_data['start_time'] + \
                    elapsed if time_data['start_time'] else None
        else:
            limit_reached_at = None
        return {
            'cost_per_hour': cost_per_hour,
            'total_cost': total_cost,
            'cost_so_far': cost_so_far,
            'cost_remaining': cost_remaining,
            'cost_limit': cost_limit,
            'limit_reached_at': limit_reached_at
        }
