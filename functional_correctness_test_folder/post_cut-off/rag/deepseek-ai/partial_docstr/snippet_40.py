
from datetime import datetime
from typing import Any, Dict, Optional


class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)"""

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
        start_time = session_data.get("start_time")
        end_time = session_data.get("end_time")

        if start_time:
            elapsed = (current_time - start_time).total_seconds()
            time_data["elapsed_seconds"] = elapsed
            time_data["elapsed_time_str"] = str(current_time - start_time)

        if end_time:
            remaining = (end_time - current_time).total_seconds()
            time_data["remaining_seconds"] = max(0, remaining)
            time_data["remaining_time_str"] = str(
                end_time - current_time) if remaining > 0 else "00:00:00"

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
        if cost_limit is None:
            cost_limit = 100.0

        cost_data = {}
        current_cost = session_data.get("current_cost", 0.0)
        cost_data["current_cost"] = current_cost

        elapsed_seconds = time_data.get("elapsed_seconds", 0.0)
        if elapsed_seconds > 0:
            cost_rate = current_cost / elapsed_seconds
            cost_data["cost_rate_per_second"] = cost_rate

            remaining_seconds = time_data.get("remaining_seconds", 0.0)
            predicted_cost = current_cost + (cost_rate * remaining_seconds)
            cost_data["predicted_cost"] = predicted_cost

            cost_limit_remaining = max(0.0, cost_limit - current_cost)
            cost_data["cost_limit_remaining"] = cost_limit_remaining

            if cost_rate > 0:
                time_to_limit = cost_limit_remaining / cost_rate
                cost_data["time_to_limit_seconds"] = time_to_limit
            else:
                cost_data["time_to_limit_seconds"] = float("inf")

        return cost_data
