from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union


class SessionCalculator:
    '''Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)'''

    def __init__(self) -> None:
        '''Initialize session calculator.'''
        pass

    @staticmethod
    def _to_datetime(value: Optional[Union[str, datetime]]) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            dt = value
        elif isinstance(value, str):
            try:
                # Handle ISO 8601 strings, including with 'Z'
                s = value.strip()
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                dt = datetime.fromisoformat(s)
            except Exception:
                return None
        else:
            return None
        # Normalize to UTC, assume naive datetimes are UTC
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    @staticmethod
    def _safe_number(value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _clip01(x: Optional[float]) -> Optional[float]:
        if x is None:
            return None
        if x < 0:
            return 0.0
        if x > 1:
            return 1.0
        return x

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        '''Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        '''
        now = self._to_datetime(current_time)
        start_time = self._to_datetime(session_data.get(
            "start_time") or session_data.get("started_at"))
        end_time = self._to_datetime(session_data.get(
            "end_time") or session_data.get("ended_at"))

        expected_duration = None
        for key in ("expected_duration_seconds", "estimated_duration_seconds", "planned_duration_seconds", "duration_seconds"):
            v = self._safe_number(session_data.get(key))
            if v is not None and v >= 0:
                expected_duration = int(v)
                break

        is_active = False
        elapsed_seconds = 0
        total_seconds = None
        remaining_seconds = None

        if start_time is not None:
            if end_time is not None and end_time >= start_time:
                elapsed_seconds = max(
                    int((end_time - start_time).total_seconds()), 0)
                is_active = False
            else:
                if now is not None and now >= start_time:
                    elapsed_seconds = max(
                        int((now - start_time).total_seconds()), 0)
                    is_active = True
                else:
                    elapsed_seconds = 0
                    is_active = False

        if expected_duration is not None:
            total_seconds = expected_duration
            if elapsed_seconds is not None:
                remaining_seconds = max(expected_duration - elapsed_seconds, 0)
        else:
            # If there's an end_time but no expected duration, total_seconds equals elapsed
            if end_time is not None and start_time is not None:
                total_seconds = elapsed_seconds

        progress = None
        if expected_duration and expected_duration > 0:
            progress = self._clip01(elapsed_seconds / expected_duration)

        result: Dict[str, Any] = {
            "current_time": now,
            "start_time": start_time,
            "end_time": end_time,
            "is_active": is_active,
            "elapsed_seconds": elapsed_seconds,
            "remaining_seconds": remaining_seconds,
            "total_seconds": total_seconds,
            "progress": progress,
        }
        return result

    def calculate_cost_predictions(self, session_data: Dict[str, Any], time_data: Dict[str, Any], cost_limit: Optional[float] = None) -> Dict[str, Any]:
        '''Calculate cost-related predictions.
        Args:
            session_data: Dictionary containing session cost information
            time_data: Time data from calculate_time_data
            cost_limit: Optional cost limit (defaults to 100.0)
        Returns:
            Dictionary with cost predictions
        '''
        # Inputs and fallbacks
        limit = 100.0 if cost_limit is None else max(float(cost_limit), 0.0)

        total_cost = self._safe_number(session_data.get("total_cost"))
        if total_cost is None:
            # Try to derive from tokens * cost_per_token
            total_tokens = self._safe_number(session_data.get("total_tokens"))
            cost_per_token = self._safe_number(
                session_data.get("cost_per_token"))
            if total_tokens is not None and cost_per_token is not None:
                total_cost = total_tokens * cost_per_token

        if total_cost is None:
            # Try time-based cost
            elapsed_seconds = time_data.get("elapsed_seconds") or 0
            cost_per_second = self._safe_number(
                session_data.get("cost_per_second"))
            if cost_per_second is not None and elapsed_seconds:
                total_cost = elapsed_seconds * cost_per_second

        if total_cost is None:
            total_cost = 0.0

        # Determine burn rate
        burn_rate_per_second = self._safe_number(
            session_data.get("cost_per_second"))
        if burn_rate_per_second is None:
            tokens_per_second = self._safe_number(
                session_data.get("tokens_per_second"))
            cost_per_token = self._safe_number(
                session_data.get("cost_per_token"))
            if tokens_per_second is not None and cost_per_token is not None:
                burn_rate_per_second = tokens_per_second * cost_per_token

        if burn_rate_per_second is None:
            elapsed_seconds = time_data.get("elapsed_seconds") or 0
            if elapsed_seconds > 0:
                burn_rate_per_second = total_cost / float(elapsed_seconds)

        if burn_rate_per_second is None or burn_rate_per_second < 0:
            burn_rate_per_second = 0.0

        remaining_seconds = time_data.get("remaining_seconds")
        expected_final_cost = None
        if remaining_seconds is not None and burn_rate_per_second > 0:
            expected_final_cost = total_cost + remaining_seconds * burn_rate_per_second

        # Limit related calculations
        cost_remaining_to_limit = max(limit - total_cost, 0.0)
        seconds_until_limit = None
        if burn_rate_per_second > 0:
            seconds_until_limit = cost_remaining_to_limit / burn_rate_per_second
        limit_exceeded = total_cost > limit + 1e-9

        can_finish_under_limit = None
        if expected_final_cost is not None:
            can_finish_under_limit = expected_final_cost <= limit + 1e-9

        predictions: Dict[str, Any] = {
            "current_cost": float(total_cost),
            "burn_rate_per_second": float(burn_rate_per_second),
            "cost_limit": float(limit),
            "cost_remaining_to_limit": float(cost_remaining_to_limit),
            "seconds_until_limit": seconds_until_limit,
            "expected_final_cost": expected_final_cost,
            "limit_exceeded": limit_exceeded,
            "can_finish_under_limit": can_finish_under_limit,
        }
        return predictions
