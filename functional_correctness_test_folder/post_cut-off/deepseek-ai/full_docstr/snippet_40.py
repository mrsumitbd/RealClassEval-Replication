
from typing import Dict, Any, Optional
from datetime import datetime


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
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time and isinstance(start_time, datetime):
            elapsed_time = current_time - start_time
            time_data['elapsed_seconds'] = elapsed_time.total_seconds()
            time_data['elapsed_time_str'] = str(elapsed_time)
        else:
            time_data['elapsed_seconds'] = 0
            time_data['elapsed_time_str'] = '00:00:00'
        return time_data

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

        cost_predictions = {}
        current_cost = session_data.get('current_cost', 0.0)
        elapsed_seconds = time_data.get('elapsed_seconds', 0)

        if elapsed_seconds > 0:
            cost_rate = current_cost / elapsed_seconds
            cost_predictions['cost_rate'] = cost_rate
            cost_predictions['projected_cost'] = cost_rate * 3600  # per hour
            # per day
            cost_predictions['projected_daily_cost'] = cost_rate * 86400
        else:
            cost_predictions['cost_rate'] = 0.0
            cost_predictions['projected_cost'] = 0.0
            cost_predictions['projected_daily_cost'] = 0.0

        cost_predictions['cost_limit'] = cost_limit
        cost_predictions['is_over_limit'] = current_cost > cost_limit

        return cost_predictions
