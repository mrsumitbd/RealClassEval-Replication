
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class SessionCalculator:
    """Handles session-related calculations for display purposes."""

    def __init__(self) -> None:
        """Initialize session calculator."""
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """Calculate time-related data for the session.

        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        """
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time:
            start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds()
            time_data['remaining_time'] = max(0, session_data.get(
                'time_limit', 0) * 60 - time_data['elapsed_time'])
        else:
            time_data['elapsed_time'] = 0
            time_data['remaining_time'] = 0
        return time_data

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        """Calculate cost-related predictions.

        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        """
        cost_predictions = {}
        cost_limit = cost_limit or 100.0
        current_cost = session_data.get('current_cost', 0)
        cost_predictions['current_cost'] = current_cost
        elapsed_time = time_data['elapsed_time']
        remaining_time = time_data['remaining_time']
        if elapsed_time > 0:
            cost_rate = current_cost / elapsed_time
            cost_predictions['predicted_cost'] = current_cost + \
                cost_rate * remaining_time
            cost_predictions['cost_exceeds_limit'] = cost_predictions['predicted_cost'] > cost_limit
        else:
            cost_predictions['predicted_cost'] = current_cost
            cost_predictions['cost_exceeds_limit'] = False
        return cost_predictions
