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
        duration = None
        elapsed = None
        remaining = None
        is_active = False

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str) and end_time:
            end_time = datetime.fromisoformat(end_time)
        else:
            end_time = None

        if start_time:
            if end_time:
                duration = end_time - start_time
                elapsed = end_time - start_time
                remaining = timedelta(0)
                is_active = False
            else:
                duration = None
                elapsed = current_time - start_time
                remaining = None
                is_active = True
        else:
            elapsed = None
            duration = None
            remaining = None
            is_active = False

        result = {
            'start_time': start_time,
            'end_time': end_time,
            'elapsed': elapsed,
            'duration': duration,
            'remaining': remaining,
            'is_active': is_active
        }
        return result

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
        total_cost = 0.0
        predicted_total_cost = None
        time_to_limit = None
        limit_reached = False

        if elapsed and isinstance(elapsed, timedelta):
            hours = elapsed.total_seconds() / 3600.0
            total_cost = cost_per_hour * hours
        else:
            hours = 0.0
            total_cost = 0.0

        # Predict total cost if session is still active
        if time_data.get('is_active'):
            # If there is a cost limit, estimate time to reach it
            if cost_per_hour > 0:
                remaining_cost = cost_limit - total_cost
                if remaining_cost > 0:
                    time_to_limit = timedelta(
                        hours=remaining_cost / cost_per_hour)
                else:
                    time_to_limit = timedelta(0)
                    limit_reached = True
            else:
                time_to_limit = None
            predicted_total_cost = None
        else:
            # Session ended, so predicted = actual
            predicted_total_cost = total_cost
            time_to_limit = timedelta(0) if total_cost >= cost_limit else None
            limit_reached = total_cost >= cost_limit

        result = {
            'cost_per_hour': cost_per_hour,
            'total_cost': total_cost,
            'predicted_total_cost': predicted_total_cost,
            'time_to_limit': time_to_limit,
            'cost_limit': cost_limit,
            'limit_reached': limit_reached
        }
        return result
