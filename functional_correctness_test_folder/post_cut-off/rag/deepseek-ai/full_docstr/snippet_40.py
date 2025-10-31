
from datetime import datetime
from typing import Dict, Any, Optional


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
            elapsed = (current_time - start_time).total_seconds()
            time_data['elapsed_seconds'] = elapsed
            time_data['elapsed_human'] = str(current_time - start_time)
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
        elapsed_seconds = time_data.get('elapsed_seconds', 0.0)

        if elapsed_seconds > 0:
            cost_rate = current_cost / elapsed_seconds
            cost_predictions['cost_rate'] = cost_rate
            cost_predictions['projected_daily_cost'] = cost_rate * 86400
            cost_predictions['time_remaining_seconds'] = (
                cost_limit - current_cost) / cost_rate if cost_rate > 0 else float('inf')
        else:
            cost_predictions['cost_rate'] = 0.0
            cost_predictions['projected_daily_cost'] = 0.0
            cost_predictions['time_remaining_seconds'] = float('inf')

        cost_predictions['current_cost'] = current_cost
        cost_predictions['cost_limit'] = cost_limit
        return cost_predictions
