
from typing import Dict, Any, Optional
from datetime import datetime


class SessionCalculator:

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        self.base_cost_per_hour = 10.0  # Assuming a base cost per hour
        self.default_cost_limit = 100.0  # Default cost limit

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''Calculate time-related data for the session.

        Args:
            session_data: Dictionary containing session information
            current_time: Current time

        Returns:
            Dictionary with time-related data
        '''
        time_data = {}
        session_start_time = session_data.get('start_time')
        if session_start_time:
            time_data['session_duration'] = (
                current_time - session_start_time).total_seconds() / 3600  # Convert to hours
            time_data['session_start_time'] = session_start_time
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
        cost_predictions = {}
        session_duration = time_data.get('session_duration', 0)
        cost_predictions['current_cost'] = session_duration * \
            self.base_cost_per_hour
        cost_limit = cost_limit if cost_limit is not None else self.default_cost_limit
        cost_predictions['cost_limit'] = cost_limit
        cost_predictions['remaining_budget'] = cost_limit - \
            cost_predictions['current_cost']
        # Simple prediction, can be improved
        cost_predictions['predicted_total_cost'] = cost_predictions['current_cost']
        return cost_predictions
