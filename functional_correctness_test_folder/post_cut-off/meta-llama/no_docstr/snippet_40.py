
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SessionCalculator:

    def __init__(self) -> None:
        """
        Initializes the SessionCalculator class.
        """
        pass

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """
        Calculates time-related data for a given session.

        Args:
        - session_data (Dict[str, Any]): Data related to the session.
        - current_time (datetime): The current time.

        Returns:
        - Dict[str, Any]: A dictionary containing time-related data.
        """
        time_data = {}
        start_time = session_data.get('start_time')
        if start_time:
            time_data['elapsed_time'] = (
                current_time - start_time).total_seconds() / 60  # in minutes
            time_data['remaining_time'] = session_data.get(
                'duration', 0) - time_data['elapsed_time']
        else:
            time_data['elapsed_time'] = 0
            time_data['remaining_time'] = session_data.get('duration', 0)
        return time_data

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculates cost predictions for a given session.

        Args:
        - session_data (Dict[str, Any]): Data related to the session.
        - time_data (Dict[str, Any]): Time-related data for the session.
        - cost_limit (Optional[float], optional): The cost limit. Defaults to None.

        Returns:
        - Dict[str, Any]: A dictionary containing cost predictions.
        """
        cost_predictions = {}
        cost_per_minute = session_data.get('cost_per_minute', 0)
        elapsed_cost = time_data['elapsed_time'] * cost_per_minute
        remaining_cost = time_data['remaining_time'] * cost_per_minute
        total_cost = elapsed_cost + remaining_cost

        cost_predictions['elapsed_cost'] = elapsed_cost
        cost_predictions['remaining_cost'] = remaining_cost
        cost_predictions['total_cost'] = total_cost

        if cost_limit is not None:
            cost_predictions['within_limit'] = total_cost <= cost_limit
            cost_predictions['cost_limit'] = cost_limit
            cost_predictions['cost_exceedance'] = max(
                0, total_cost - cost_limit)

        return cost_predictions
