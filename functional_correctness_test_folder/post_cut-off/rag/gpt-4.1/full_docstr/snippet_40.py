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
        if end_time and isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)
        if paused_time and isinstance(paused_time, str):
            paused_time = datetime.fromisoformat(paused_time)
        if isinstance(total_paused_duration, (int, float)):
            total_paused_duration = timedelta(seconds=total_paused_duration)

        # If session is paused, add the current paused duration
        if is_paused and paused_time:
            paused_duration = current_time - paused_time
            total_paused = total_paused_duration + paused_duration
        else:
            total_paused = total_paused_duration

        # Compute elapsed time
        if end_time:
            elapsed = end_time - start_time - total_paused
            is_active = False
        else:
            elapsed = current_time - start_time - total_paused
            is_active = True

        elapsed_seconds = max(int(elapsed.total_seconds()), 0)

        return {
            'start_time': start_time,
            'end_time': end_time,
            'is_paused': is_paused,
            'paused_time': paused_time,
            'total_paused_duration': total_paused,
            'elapsed': elapsed,
            'elapsed_seconds': elapsed_seconds,
            'is_active': is_active,
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
        elapsed_seconds = time_data.get('elapsed_seconds', 0)
        elapsed_hours = elapsed_seconds / 3600.0

        current_cost = hourly_rate * elapsed_hours

        # Predict time to reach cost limit
        if hourly_rate > 0:
            remaining_cost = max(cost_limit - current_cost, 0)
            hours_left = remaining_cost / hourly_rate
            seconds_left = int(hours_left * 3600)
            predicted_end_time = None
            if time_data.get('is_active', True):
                predicted_end_time = datetime.utcnow() + timedelta(seconds=seconds_left)
        else:
            hours_left = None
            seconds_left = None
            predicted_end_time = None

        return {
            'current_cost': current_cost,
            'cost_limit': cost_limit,
            'remaining_cost': max(cost_limit - current_cost, 0),
            'hours_left': hours_left,
            'seconds_left': seconds_left,
            'predicted_end_time': predicted_end_time,
        }
