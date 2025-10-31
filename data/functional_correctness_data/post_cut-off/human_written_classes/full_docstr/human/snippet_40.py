from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from claude_monitor.utils.time_utils import TimezoneHandler, format_display_time, get_time_format_preference, percentage

class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)"""

    def __init__(self) -> None:
        """Initialize session calculator."""
        self.tz_handler = TimezoneHandler()

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """Calculate time-related data for the session.

        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time

        Returns:
            Dictionary with calculated time data
        """
        start_time = None
        if session_data.get('start_time_str'):
            start_time = self.tz_handler.parse_timestamp(session_data['start_time_str'])
            start_time = self.tz_handler.ensure_utc(start_time)
        if session_data.get('end_time_str'):
            reset_time = self.tz_handler.parse_timestamp(session_data['end_time_str'])
            reset_time = self.tz_handler.ensure_utc(reset_time)
        else:
            reset_time = start_time + timedelta(hours=5) if start_time else current_time + timedelta(hours=5)
        time_to_reset = reset_time - current_time
        minutes_to_reset = time_to_reset.total_seconds() / 60
        if start_time and session_data.get('end_time_str'):
            total_session_minutes = (reset_time - start_time).total_seconds() / 60
            elapsed_session_minutes = (current_time - start_time).total_seconds() / 60
            elapsed_session_minutes = max(0, elapsed_session_minutes)
        else:
            total_session_minutes = 5 * 60
            elapsed_session_minutes = max(0, total_session_minutes - minutes_to_reset)
        return {'start_time': start_time, 'reset_time': reset_time, 'minutes_to_reset': minutes_to_reset, 'total_session_minutes': total_session_minutes, 'elapsed_session_minutes': elapsed_session_minutes}

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float]=None) -> Dict[str, Any]:
        """Calculate cost-related predictions.

        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)

        Returns:
            Dictionary with cost predictions
        """
        elapsed_minutes = time_data['elapsed_session_minutes']
        session_cost = session_data.get('session_cost', 0.0)
        current_time = datetime.now(timezone.utc)
        cost_per_minute = session_cost / max(1, elapsed_minutes) if elapsed_minutes > 0 else 0
        if cost_limit is None:
            cost_limit = 100.0
        cost_remaining = max(0, cost_limit - session_cost)
        if cost_per_minute > 0 and cost_remaining > 0:
            minutes_to_cost_depletion = cost_remaining / cost_per_minute
            predicted_end_time = current_time + timedelta(minutes=minutes_to_cost_depletion)
        else:
            predicted_end_time = time_data['reset_time']
        return {'cost_per_minute': cost_per_minute, 'cost_limit': cost_limit, 'cost_remaining': cost_remaining, 'predicted_end_time': predicted_end_time}