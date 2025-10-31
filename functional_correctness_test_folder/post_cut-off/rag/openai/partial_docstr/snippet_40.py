
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        # Default cost limit used when none is supplied
        self.default_cost_limit = 100.0

    def _parse_time(self, value: Any) -> Optional[datetime]:
        '''Parse a datetime value that may be a datetime instance or an ISO string.'''
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Python 3.7+ supports fromisoformat for most ISO strings
                return datetime.fromisoformat(value)
            except Exception:
                # Try common formats
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                    try:
                        return datetime.strptime(value, fmt)
                    except Exception:
                        continue
        return None

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        '''
        start_time = self._parse_time(session_data.get('start_time'))
        end_time = self._parse_time(session_data.get('end_time'))

        # If duration is provided but end_time missing, compute end_time
        if end_time is None and start_time is not None:
            duration_sec = session_data.get('duration')
            if isinstance(duration_sec, (int, float)):
                end_time = start_time + timedelta(seconds=duration_sec)

        # Compute elapsed
        elapsed = None
        if start_time is not None:
            elapsed = current_time - start_time
            if elapsed.total_seconds() < 0:
                elapsed = timedelta(seconds=0)

        # Compute remaining
        remaining = None
        if end_time is not None:
            remaining = end_time - current_time
            if remaining.total_seconds() < 0:
                remaining = timedelta(seconds=0)

        # Compute total
        total = None
        if start_time is not None and end_time is not None:
            total = end_time - start_time
            if total.total_seconds() < 0:
                total = timedelta(seconds=0)

        # Build result
        result: Dict[str, Any] = {}
        if elapsed is not None:
            result['elapsed_seconds'] = elapsed.total_seconds()
            result['elapsed_hours'] = elapsed.total_seconds() / 3600.0
            result['elapsed_time'] = elapsed
        if remaining is not None:
            result['remaining_seconds'] = remaining.total_seconds()
            result['remaining_hours'] = remaining.total_seconds() / 3600.0
            result['remaining_time'] = remaining
        if total is not None:
            result['total_seconds'] = total.total_seconds()
            result['total_hours'] = total.total_seconds() / 3600.0
            result['total_time'] = total

        # Active flag
        result['is_active'] = bool(start_time and (
            end_time is None or current_time < end_time))

        return result

    def calculate_cost_predictions(
        self,
        session_data: Dict[str, Any],
        time_data: Dict[str, Any],
        cost_limit: Optional[float] = None
    ) -> Dict[str, Any]:
        '''Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        '''
        # Determine cost limit
        limit = cost_limit if cost_limit is not None else self.default_cost_limit

        # Current cost
        current_cost = session_data.get('current_cost', 0.0)
        try:
            current_cost = float(current_cost)
        except Exception:
            current_cost = 0.0

        # Cost per hour
        cost_per_hour = session_data.get('cost_per_hour', 0.0)
        try:
            cost_per_hour = float(cost_per_hour)
        except Exception:
            cost_per_hour = 0.0

        # Remaining time in seconds
        remaining_seconds = time_data.get('remaining_seconds')
        if remaining_seconds is None:
            remaining_seconds = 0.0
        try:
            remaining_seconds = float(remaining_seconds)
        except Exception:
            remaining_seconds = 0.0

        # Predicted additional cost
        remaining_hours = remaining_seconds / 3600.0
        predicted_additional = cost_per_hour * remaining_hours

        # Total predicted cost
        predicted_total = current_cost + predicted_additional

        # Hours until limit
        hours_until_limit = None
        if cost_per_hour > 0:
            remaining_budget = limit - current_cost
            if remaining_budget > 0:
                hours_until_limit = remaining_budget / cost_per_hour
            else:
                hours_until_limit = 0.0

        # Build result
        result: Dict[str, Any] = {
            'current_cost': current_cost,
            'cost_per_hour': cost_per_hour,
            'predicted_additional_cost': predicted_additional,
            'predicted_total_cost': predicted_total,
            'cost_limit': limit
