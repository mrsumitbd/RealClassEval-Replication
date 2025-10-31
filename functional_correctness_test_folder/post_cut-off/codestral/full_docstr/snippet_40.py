
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
        if start_time:
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds() / 3600  # in hours
        else:
            time_data['elapsed_time'] = 0.0

        time_data['current_time'] = current_time
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
        cost_rate = session_data.get('cost_rate', 0.0)
        elapsed_time = time_data.get('elapsed_time', 0.0)

        cost_predictions['current_cost'] = cost_rate * elapsed_time
        cost_predictions['remaining_cost'] = max(
            0.0, cost_limit - cost_predictions['current_cost'])
        cost_predictions['remaining_time'] = cost_predictions['remaining_cost'] / \
            cost_rate if cost_rate > 0 else 0.0

        return cost_predictions
