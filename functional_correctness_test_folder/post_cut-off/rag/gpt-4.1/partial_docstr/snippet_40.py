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
        start_time = session_data.get('start_time')
        end_time = session_data.get('end_time')
        paused_time = session_data.get('paused_time')
        total_paused_duration = session_data.get(
            'total_paused_duration', timedelta(0))
        is_paused = session_data.get('is_paused', False)

        # Parse times if they are strings
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str) and end_time:
            end_time = datetime.fromisoformat(end_time)
        if isinstance(paused_time, str) and paused_time:
            paused_time = datetime.fromisoformat(paused_time)
        if isinstance(total_paused_duration, (int, float)):
            total_paused_duration = timedelta(seconds=total_paused_duration)

        # Calculate elapsed time
        if end_time:
            elapsed = end_time - start_time
        else:
            elapsed = current_time - start_time

        # Subtract paused duration
        if is_paused and paused_time:
            paused_elapsed = current_time - paused_time
            total_paused = total_paused_duration + paused_elapsed
        else:
            total_paused = total_paused_duration

        active_time = elapsed - total_paused
        if active_time.total_seconds() < 0:
            active_time = timedelta(0)

        return {
            'start_time': start_time,
            'end_time': end_time,
            'current_time': current_time,
            'elapsed': elapsed,
            'total_paused': total_paused,
            'active_time': active_time,
            'is_paused': is_paused,
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
        active_time = time_data.get('active_time', timedelta(0))
        elapsed_hours = active_time.total_seconds() / 3600.0

        current_cost = hourly_rate * elapsed_hours

        # Predict time to reach cost limit
        if hourly_rate > 0:
            remaining_cost = max(0.0, cost_limit - current_cost)
            hours_left = remaining_cost / hourly_rate
            time_to_limit = timedelta(hours=hours_left)
            predicted_end_time = time_data['current_time'] + time_to_limit
        else:
            time_to_limit = None
            predicted_end_time = None

        return {
            'current_cost': current_cost,
            'cost_limit': cost_limit,
            'hourly_rate': hourly_rate,
            'time_to_limit': time_to_limit,
            'predicted_end_time': predicted_end_time,
        }
