
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)
    """

    def __init__(self) -> None:
        """Initialize session calculator."""
        # Default cost per hour if not provided in session data
        self.default_cost_per_hour: float = 100.0

    def _ensure_datetime(self, value: Any) -> Optional[datetime]:
        """Try to convert a value to datetime, return None if impossible."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except Exception:
                return None
        return None

    def calculate_time_data(
        self, session_data: Dict[str, Any], current_time: datetime
    ) -> Dict[str, Any]:
        """Calculate time-related data for the session.

        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time

        Returns:
            Dictionary with calculated time data
        """
        start_time = self._ensure_datetime(session_data.get("start_time"))
        end_time = self._ensure_datetime(session_data.get("end_time"))

        if not start_time:
            # If no start time, nothing to calculate
            return {
                "elapsed_seconds": 0,
                "elapsed_minutes": 0,
                "elapsed_hours": 0,
                "remaining_seconds": None,
                "remaining_minutes": None,
                "remaining_hours": None,
                "percent_elapsed": 0.0,
                "is_active": False,
                "is_finished": False,
            }

        # Elapsed time
        elapsed = current_time - start_time
        elapsed_seconds = max(0, int(elapsed.total_seconds()))
        elapsed_minutes = elapsed_seconds // 60
        elapsed_hours = elapsed_seconds // 3600

        # Remaining time if end_time is known
        if end_time and end_time > start_time:
            remaining = end_time - current_time
            remaining_seconds = max(0, int(remaining.total_seconds()))
            remaining_minutes = remaining_seconds // 60
            remaining_hours = remaining_seconds // 3600
            total_duration_seconds = int(
                (end_time - start_time).total_seconds())
            percent_elapsed = (
                elapsed_seconds / total_duration_seconds if total_duration_seconds else 0.0
            )
            is_active = current_time < end_time
            is_finished = current_time >= end_time
        else:
            remaining_seconds = None
            remaining_minutes = None
            remaining_hours = None
            percent_elapsed = 0.0
            is_active = True
            is_finished = False

        return {
            "elapsed_seconds": elapsed_seconds,
            "elapsed_minutes": elapsed_minutes,
            "elapsed_hours": elapsed_hours,
            "remaining_seconds": remaining_seconds,
            "remaining_minutes": remaining_minutes,
            "remaining_hours": remaining_hours,
            "percent_elapsed": percent_elapsed,
            "is_active": is_active,
            "is_finished": is_finished,
        }

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Calculate cost-related predictions.

        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)

        Returns:
            Dictionary with cost predictions
        """
        # Determine cost per second
        cost_per_second: Optional[float] = None
        if "cost_per_second" in session_data:
            cost_per_second = float(session_data["cost_per_second"])
        elif "cost_per_minute" in session_data:
            cost_per_second = float(session_data["cost_per_minute"]) / 60.0
        elif "cost_per_hour" in session_data:
            cost_per_second = float(session_data["cost_per_hour"]) / 3600.0
        else:
            # Use default if nothing provided
            cost_per_second = self.default_cost_per_hour / 3600.0

        elapsed_seconds = time_data.get("elapsed_seconds", 0)
        remaining_seconds = time_data.get("remaining_seconds")
        if remaining_seconds is None:
            remaining_seconds = 0

        cost_so_far = elapsed_seconds * cost_per_second
        cost_remaining = remaining_seconds * cost_per_second
        total_predicted_cost = cost_so_far + cost_remaining

        # Handle cost limit
        if cost_limit is None:
            cost_limit = self.default_cost_per_hour
        cost_limit_remaining = cost_limit - cost_so_far
        over_limit = cost_so_far > cost_limit

        return {
            "cost_per_second": cost_per_second,
            "cost_so_far": cost_so_far,
            "cost_remaining": cost_remaining,
            "total_predicted_cost": total_predicted_cost,
            "cost_limit": cost_limit,
            "cost_limit_remaining": cost_limit_remaining,
            "over_limit": over_limit,
        }
