
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    """
    A simple calculator for session timing and cost predictions.

    Expected keys in ``session_data``:
        - ``start_time`` (datetime): when the session started.
        - ``duration_minutes`` (int): total planned duration in minutes.
        - ``cost_per_minute`` (float): cost rate per minute.

    The methods return dictionaries with computed values.
    """

    def __init__(self) -> None:
        pass

    def calculate_time_data(
        self, session_data: Dict[str, Any], current_time: datetime
    ) -> Dict[str, Any]:
        """
        Compute timing information for a session.

        Parameters
        ----------
        session_data : dict
            Dictionary containing at least ``start_time`` and ``duration_minutes``.
        current_time : datetime
            The current timestamp to compare against the session start.

        Returns
        -------
        dict
            Contains:
                - ``elapsed_minutes`` (float)
                - ``remaining_minutes`` (float)
                - ``percentage_complete`` (float, 0‑100)
                - ``end_time`` (datetime)
        """
        # Extract required values with defaults
        start_time: datetime = session_data.get("start_time", current_time)
        duration_minutes: int = session_data.get("duration_minutes", 0)
        cost_per_minute: float = session_data.get("cost_per_minute", 0.0)

        # Compute end time
        end_time = start_time + timedelta(minutes=duration_minutes)

        # Compute elapsed time in minutes
        elapsed = max(0.0, (current_time - start_time).total_seconds() / 60.0)

        # Compute remaining time
        remaining = max(0.0, duration_minutes - elapsed)

        # Compute percentage complete
        percentage = (
            (elapsed / duration_minutes) *
            100.0 if duration_minutes > 0 else 0.0
        )

        return {
            "elapsed_minutes": elapsed,
            "remaining_minutes": remaining,
            "percentage_complete": percentage,
            "end_time": end_time,
            "cost_per_minute": cost_per_minute,
        }

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Predict costs for a session based on timing data.

        Parameters
        ----------
        session_data : dict
            Original session data (may contain ``cost_per_minute``).
        time_data : dict
            Output from :meth:`calculate_time_data`.
        cost_limit : float, optional
            If provided, indicates a maximum acceptable cost.

        Returns
        -------
        dict
            Contains:
                - ``total_cost`` (float)
                - ``cost_so_far`` (float)
                - ``cost_remaining`` (float)
                - ``cost_limit_exceeded`` (bool, if cost_limit is set)
        """
        # Retrieve cost rate
        cost_per_minute: float = time_data.get("cost_per_minute", 0.0)

        # Compute costs
        elapsed = time_data.get("elapsed_minutes", 0.0)
        remaining = time_data.get("remaining_minutes", 0.0)

        cost_so_far = elapsed * cost_per_minute
        cost_remaining = remaining * cost_per_minute
        total_cost = cost_so_far + cost_remaining

        result: Dict[str, Any] = {
            "total_cost": total_cost,
            "cost_so_far": cost_so_far,
            "cost_remaining": cost_remaining,
        }

        if cost_limit is not None:
            result["cost_limit_exceeded"] = total_cost > cost_limit

        return result
