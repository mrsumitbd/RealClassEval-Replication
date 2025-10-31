
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        # No state needed for this calculator
        pass

    def _parse_datetime(self, value: Any) -> Optional[datetime]:
        """Attempt to parse a datetime from a string or return None."""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Try ISO format first
                return datetime.fromisoformat(value)
            except ValueError:
                try:
                    # Fallback to common formats
                    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return None
        return None

    def calculate_time_data(
        self, session_data: Dict[str, Any], current_time: datetime
    ) -> Dict[str, Any]:
        '''Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        '''
        start = self._parse_datetime(session_data.get("start_time"))
        end = self._parse_datetime(session_data.get("end_time"))

        # Compute elapsed, remaining, and total duration
        elapsed = None
        remaining = None
        duration = None

        if start:
            elapsed = current_time - start
            elapsed_seconds = max(elapsed.total_seconds(), 0)
        else:
            elapsed_seconds = None

        if end:
            remaining = end - current_time
            remaining_seconds = max(remaining.total_seconds(), 0)
        else:
            remaining_seconds = None

        if start and end:
            duration = end - start
            duration_seconds = max(duration.total_seconds(), 0)
        else:
            duration_seconds = None

        # Build result dictionary
        result: Dict[str, Any] = {
            "start_time": start,
            "end_time": end,
            "elapsed": elapsed,
            "remaining": remaining,
            "duration": duration,
            "elapsed_seconds": elapsed_seconds,
            "remaining_seconds": remaining_seconds,
            "duration_seconds": duration_seconds,
        }

        # Add convenience numeric fields if available
        if elapsed_seconds is not None:
            result["elapsed_minutes"] = elapsed_seconds / 60
            result["elapsed_hours"] = elapsed_seconds / 3600
        if remaining_seconds is not None:
            result["remaining_minutes"] = remaining_seconds / 60
            result["remaining_hours"] = remaining_seconds / 3600
        if duration_seconds is not None:
            result["duration_minutes"] = duration_seconds / 60
            result["duration_hours"] = duration_seconds / 3600

        return result

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None,
    ) -> Dict[str, Any]:
        '''Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        '''
        # Default cost limit
        if cost_limit is None:
            cost_limit = 100.0

        # Determine cost per second
        cost_per_minute = session_data.get("cost_per_minute")
        cost_per_hour = session_data.get("cost_per_hour")

        if cost_per_minute is not None:
            try:
                cost_per_second = float(cost_per_minute) / 60.0
            except (TypeError, ValueError):
                cost_per_second = 0.0
        elif cost_per_hour is not None:
            try:
                cost_per_second = float(cost_per_hour) / 3600.0
            except (TypeError, ValueError):
                cost_per_second = 0.0
        else:
            cost_per_second = 0.0

        # Elapsed seconds from time_data
        elapsed_seconds = time_data.get("elapsed_seconds")
        if elapsed_seconds is None:
            elapsed_seconds = 0.0

        # Total session seconds
        total_seconds = time_data.get("duration_seconds")
        if total_seconds is None:
            total_seconds = elapsed_seconds  # fallback

        # Current and projected costs
        current_cost = cost_per_second * elapsed_seconds
        projected_cost = cost_per_second * total_seconds

        over_limit = projected_cost > cost_limit

        result: Dict[str, Any] = {
            "cost_per_second": cost_per_second,
            "elapsed_seconds": elapsed_seconds,
            "total_seconds": total_seconds,
            "current_cost": current_cost,
            "projected_cost": projected_cost,
            "cost_limit": cost_limit,
            "over_limit": over_limit,
        }

        # Add human‑readable fields
        result["current_cost_formatted"] = f"${current_cost:,.2f}"
        result["projected_cost_formatted"] = f"${projected_cost:,.2f}"
        result["cost_limit_formatted"] = f"${cost_limit:,.2f}"

        return result
