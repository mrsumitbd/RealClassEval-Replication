
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
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time:
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds()
            time_data['remaining_time'] = session_data.get(
                'duration', 0) - time_data['elapsed_time']
            time_data['end_time'] = start_time + \
                timedelta(seconds=session_data.get('duration', 0))
        else:
            time_data['elapsed_time'] = 0
            time_data['remaining_time'] = 0
            time_data['end_time'] = None
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
        cost_predictions = {}
        cost_per_hour = session_data.get('cost_per_hour', 0)
        elapsed_time_hours = time_data['elapsed_time'] / 3600
        cost_predictions['current_cost'] = cost_per_hour * elapsed_time_hours
        if cost_limit is None:
            cost_limit = 100.0
        cost_predictions['cost_limit'] = cost_limit
        cost_predictions['exceeds_limit'] = cost_predictions['current_cost'] > cost_limit
        if time_data['remaining_time'] > 0:
            cost_predictions['predicted_cost'] = cost_per_hour * \
                (elapsed_time_hours + (time_data['remaining_time'] / 3600))
        else:
            cost_predictions['predicted_cost'] = cost_predictions['current_cost']
        return cost_predictions
