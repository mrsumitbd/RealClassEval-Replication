
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    """
    A utility class for calculating time and cost predictions for a session.
    """

    def __init__(self) -> None:
        """Initialize session calculator."""
        # No state is required for this simple calculator.
        pass

    def calculate_time_data(
        self, session_data: Dict[str, Any], current_time: datetime
    ) -> Dict[str, Any]:
        """
        Calculate elapsed and remaining time information for a session.

        Parameters
        ----------
        session_data : dict
            Dictionary containing at least the keys:
                - 'start_time' (datetime): when the session started.
                - 'duration' (timedelta or int): total expected duration of the session.
        current_time : datetime
            The current timestamp to compare against the session start.

        Returns
        -------
        dict
            Dictionary with keys:
                - 'elapsed' (timedelta): time elapsed since start.
                - 'remaining' (timedelta): time remaining until the session ends.
                - 'percentage' (float): percentage of the session that has elapsed.
        """
        # Extract start time and duration
        start_time = session_data.get("start_time")
        duration = session_data.get("duration")

        if start_time is None or duration is None:
            raise ValueError(
                "session_data must contain 'start_time' and 'duration' keys"
            )

        # Ensure duration is a timedelta
        if isinstance(duration, (int, float)):
            duration = timedelta(seconds=duration)

        # Compute elapsed time
        elapsed = current_time - start_time
        if elapsed < timedelta(0):
            elapsed = timedelta(0)

        # Compute remaining time
        remaining = duration - elapsed
        if remaining < timedelta(0):
            remaining = timedelta(0)

        # Compute percentage
        total_seconds = duration.total_seconds()
        elapsed_seconds = elapsed.total_seconds()
        percentage = (elapsed_seconds / total_seconds) * \
            100 if total_seconds > 0 else 0.0

        return {
            "elapsed": elapsed,
            "remaining": remaining,
            "percentage": percentage,
        }

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Calculate cost-related predictions for a session.

        Parameters
        ----------
        session_data : dict
            Dictionary containing at least the keys:
                - 'cost_per_minute' (float): cost rate per minute.
                - 'duration' (timedelta or int): total expected duration of the session.
        time_data : dict
            Dictionary returned by `calculate_time_data`, containing at least:
                - 'elapsed' (timedelta)
                - 'remaining' (timedelta)
        cost_limit : float, optional
            Optional cost limit. If provided, the calculator will estimate how many
            minutes remain before the limit is reached. Defaults to 100.0.

        Returns
        -------
        dict
            Dictionary with keys:
                - 'predicted_total_cost' (float): cost for the entire session.
                - 'predicted_remaining_cost' (float): cost for the remaining time.
                - 'minutes_until_limit' (float or None): minutes until the cost limit
                  is reached, or None if the limit is not exceeded.
        """
        # Default cost limit
        if cost_limit is None:
            cost_limit = 100.0

        # Extract required values
        cost_per_minute = session_data.get("cost_per_minute")
        duration = session_data.get("duration")
        elapsed = time_data.get("elapsed")
        remaining = time_data.get("remaining")

        if cost_per_minute is None or duration is None or elapsed is None or remaining is None:
            raise ValueError(
                "Missing required keys in session_data or time_data for cost calculation"
            )

        # Ensure duration is a timedelta
        if isinstance(duration, (int, float)):
            duration = timedelta(seconds=duration)

        # Convert timedeltas to minutes
        total_minutes = duration.total_seconds() / 60
        elapsed_minutes = elapsed.total_seconds() / 60
        remaining_minutes = remaining.total_seconds() / 60

        # Predicted costs
        predicted_total_cost = cost_per_minute * total_minutes
        predicted_remaining_cost = cost_per_minute * remaining_minutes

        # Minutes until cost limit
        if predicted_total_cost > cost_limit:
            # Already exceeded limit
            minutes_until_limit = 0.0
        else:
            # Estimate minutes until reaching the limit
            remaining_cost_to_limit = cost_limit - predicted_total_cost
            minutes_until_limit = remaining_cost_to_limit / cost_per_minute

        return {
            "predicted_total_cost": predicted_total_cost,
            "predicted_remaining_cost": predicted_remaining_cost,
            "minutes_until_limit": minutes_until_limit,
        }
