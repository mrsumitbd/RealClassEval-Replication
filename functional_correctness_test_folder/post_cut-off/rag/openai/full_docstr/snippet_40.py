
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        # Default cost limit used when none is supplied
        self.default_cost_limit = 100.0

    @staticmethod
    def _parse_time(value: Any) -> Optional[datetime]:
        '''Parse a datetime value that may be a datetime instance or an ISO string.'''
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                # Try ISO format with timezone
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except Exception:
                try:
                    # Fallback to common UTC format
                    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
                except Exception:
                    return None
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

        # Ensure current_time is timezone-aware UTC
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        elapsed_seconds = 0.0
        remaining_seconds = None
        is_active = False
        is_finished = False

        if start_time:
            if current_time >= start_time:
                elapsed_seconds = (current_time - start_time).total_seconds()
                is_active = True
            else:
                # Session hasn't started yet
                elapsed_seconds = 0.0
                is_active = False

        if end_time:
            if current_time < end_time:
                remaining_seconds = (end_time - current_time).total_seconds()
                is_active = is_active and True
            else:
                remaining_seconds = 0.0
                is_active = False
                is_finished = True
        else:
            # No explicit end time; treat as ongoing
            remaining_seconds = None

        # Time until next hour boundary (for billing granularity)
        next_hour = (current_time.replace(minute=0, second=0,
                     microsecond=0) + timedelta(hours=1))
        seconds_to_next_hour = (next_hour - current_time).total_seconds()

        return {
            'start_time': start_time,
            'end_time': end_time,
            'current_time': current_time,
            'elapsed_seconds': elapsed_seconds,
            'remaining_seconds': remaining_seconds,
            'is_active': is_active,
            'is_finished': is_finished,
            'seconds_to_next_hour': seconds_to_next_hour,
        }

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
        # Extract cost parameters
        cost_per_hour = session_data.get('cost_per_hour')
        if cost_per_hour is None:
            # Try alternative key names
            cost_per_hour = session_data.get('cost_per_node_per_hour')
        if cost_per_hour is None:
            cost_per_hour = 0.0

        node_count = session_data.get('node_count')
        if node_count is None:
            node_count = session_data.get('num_nodes')
        if node_count is None:
            node_count = 1

        # Use provided cost limit or default
        limit = cost_limit if cost_limit is not None else self.default_cost_limit

        elapsed_seconds = time_data.get('elapsed_seconds', 0.0)
        remaining_seconds = time_data.get('remaining_seconds')
        if remaining_seconds is None:
            remaining_seconds = 0.0

        elapsed_hours = elapsed_seconds / 3600.0
        remaining_hours = remaining_seconds / 3600.0

        elapsed_cost = cost_per_hour * node_count * elapsed_hours
        remaining_cost = cost_per_hour * node_count * remaining_hours
        predicted_total_cost = elapsed_cost + remaining_cost

        cost_limit_exceeded = predicted_total_cost > limit

        return {
            'cost_per_hour': cost_per_hour,
            'node_count': node_count,
            'elapsed_hours': elapsed_hours,
            'remaining_hours': remaining_hours,
            'elapsed_cost': elapsed_cost,
            'remaining_cost': remaining_cost,
            'predicted_total_cost': predicted_total_cost,
            'cost_limit': limit,
            'cost_limit_exceeded': cost_limit_exceeded,
        }
