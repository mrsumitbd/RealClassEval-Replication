from typing import Any, Dict, Optional, List
from datetime import datetime, timezone, timedelta


class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)"""

    def __init__(self) -> None:
        """Initialize session calculator."""
        self.default_cost_limit: float = 100.0
        self.heartbeat_stale_after_seconds: int = 600

        self._start_keys: List[str] = [
            "start_time", "started_at", "created_at", "launched_at", "start"
        ]
        self._end_keys: List[str] = [
            "end_time", "ended_at", "stopped_at", "terminated_at", "finished_at", "completed_at", "end"
        ]
        self._heartbeat_keys: List[str] = [
            "last_heartbeat", "heartbeat_at", "last_activity_at", "last_ping_at", "updated_at"
        ]
        self._status_keys: List[str] = [
            "status", "state", "lifecycle"
        ]
        self._hourly_rate_keys: List[str] = [
            "hourly_rate", "rate_per_hour", "cost_per_hour", "price_per_hour",
            "spend_rate", "burn_rate", "dollars_per_hour", "node_hourly_cost",
            "instance_rate_per_hour"
        ]
        self._accrued_cost_keys: List[str] = [
            "accrued_cost", "total_cost", "cost", "spend", "amount_billed", "amount", "bill_to_date"
        ]

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        """
        now = self._ensure_aware_utc(current_time)

        start_dt = self._get_datetime_from_keys(session_data, self._start_keys)
        end_dt = self._get_datetime_from_keys(session_data, self._end_keys)
        hb_dt = self._get_datetime_from_keys(
            session_data, self._heartbeat_keys)

        status_val = self._get_first_value(session_data, self._status_keys)
        status_str = str(status_val).lower(
        ) if status_val is not None else None

        seconds_since_heartbeat = None
        heartbeat_stale = False
        if hb_dt is not None:
            seconds_since_heartbeat = max(0, (now - hb_dt).total_seconds())
            heartbeat_stale = seconds_since_heartbeat > self.heartbeat_stale_after_seconds

        is_running_by_status = False
        if status_str is None:
            is_running_by_status = True
        else:
            running_set = {"running", "active", "up",
                           "alive", "started", "pending", "provisioning"}
            stopped_set = {"stopped", "terminated", "completed",
                           "failed", "error", "paused", "succeeded", "finished"}
            if status_str in running_set:
                is_running_by_status = True
            elif status_str in stopped_set:
                is_running_by_status = False
            else:
                is_running_by_status = True

        is_running = (
            end_dt is None) and is_running_by_status and not heartbeat_stale

        if start_dt is None:
            elapsed_seconds = 0.0
        else:
            end_ref = now if end_dt is None else end_dt
            elapsed_seconds = max(0.0, (end_ref - start_dt).total_seconds())

        time_data: Dict[str, Any] = {
            "now": now,
            "now_iso": now.isoformat(),

            "start_time": start_dt,
            "start_time_iso": start_dt.isoformat() if start_dt else None,

            "end_time": end_dt,
            "end_time_iso": end_dt.isoformat() if end_dt else None,

            "last_heartbeat": hb_dt,
            "last_heartbeat_iso": hb_dt.isoformat() if hb_dt else None,

            "seconds_since_heartbeat": seconds_since_heartbeat,
            "heartbeat_stale": heartbeat_stale,

            "is_running": is_running,
            "status": status_val,

            "elapsed_seconds": elapsed_seconds,
            "elapsed_hours": elapsed_seconds / 3600.0 if elapsed_seconds else 0.0,
            "elapsed_str": self._format_hms(elapsed_seconds),
        }
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
        now: datetime = time_data.get("now") or self._ensure_aware_utc(
            datetime.now(timezone.utc))
        is_running: bool = bool(time_data.get("is_running", False))

        hourly_rate = self._get_numeric_from_keys(
            session_data, self._hourly_rate_keys, default=0.0)
        accrued_cost = self._get_numeric_from_keys(
            session_data, self._accrued_cost_keys, default=0.0)

        limit = self.default_cost_limit if cost_limit is None else float(
            cost_limit)
        remaining_budget = max(0.0, limit - accrued_cost)

        hours_until_limit = None
        seconds_until_limit = None
        end_time_at_limit = None

        if is_running and hourly_rate and hourly_rate > 0:
            hours_until_limit = remaining_budget / \
                hourly_rate if remaining_budget > 0 else 0.0
            seconds_until_limit = max(0.0, hours_until_limit * 3600.0)
            if hours_until_limit == 0.0 and remaining_budget == 0.0:
                end_time_at_limit = now
            elif hours_until_limit is not None:
                end_time_at_limit = now + timedelta(hours=hours_until_limit)

        projected_cost_next_1h = hourly_rate if is_running else 0.0
        projected_cost_next_8h = hourly_rate * 8 if is_running else 0.0
        projected_cost_next_24h = hourly_rate * 24 if is_running else 0.0

        end_of_day_utc = datetime(
            year=now.year, month=now.month, day=now.day, tzinfo=timezone.utc) + timedelta(days=1)
        hours_remaining_today = max(
            0.0, (end_of_day_utc - now).total_seconds() / 3600.0)
        projected_cost_till_eod = hourly_rate * \
            hours_remaining_today if is_running else 0.0

        predictions: Dict[str, Any] = {
            "hourly_rate": float(hourly_rate),
            "accrued_cost": float(accrued_cost),

            "projected_cost_per_day": float(hourly_rate * 24.0),
            "projected_cost_per_week": float(hourly_rate * 24.0 * 7.0),
            "projected_cost_per_30d": float(hourly_rate * 24.0 * 30.0),

            "projected_cost_next_1h": float(projected_cost_next_1h),
            "projected_cost_next_8h": float(projected_cost_next_8h),
            "projected_cost_next_24h": float(projected_cost_next_24h),
            "projected_cost_till_eod_utc": float(projected_cost_till_eod),

            "cost_limit": float(limit),
            "remaining_budget": float(remaining_budget),

            "hours_until_limit": hours_until_limit,
            "seconds_until_limit": seconds_until_limit,
            "end_time_at_limit": end_time_at_limit,
            "end_time_at_limit_iso": end_time_at_limit.isoformat() if end_time_at_limit else None,
        }
        return predictions

    def _get_first_value(self, data: Dict[str, Any], keys: List[str]) -> Any:
        for k in keys:
            if k in data and data[k] is not None:
                return data[k]
        return None

    def _get_datetime_from_keys(self, data: Dict[str, Any], keys: List[str]) -> Optional[datetime]:
        val = self._get_first_value(data, keys)
        return self._to_datetime(val)

    def _get_numeric_from_keys(self, data: Dict[str, Any], keys: List[str], default: float = 0.0) -> float:
        val = self._get_first_value(data, keys)
        if val is None:
            return float(default)
        try:
            return float(val)
        except (TypeError, ValueError):
            return float(default)

    def _to_datetime(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return self._ensure_aware_utc(value)
        if isinstance(value, (int, float)):
            # Assume epoch seconds
            return datetime.fromtimestamp(float(value), tz=timezone.utc)
        if isinstance(value, str):
            try:
                # Python 3.11: fromisoformat supports 'Z'. Replace Z with +00:00 for older versions.
                iso_str = value.replace(
                    "Z", "+00:00") if value.endswith("Z") else value
                dt = datetime.fromisoformat(iso_str)
                return self._ensure_aware_utc(dt)
            except Exception:
                return None
        return None

    def _ensure_aware_utc(self, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _format_hms(self, seconds: float) -> str:
        seconds_int = int(max(0, round(seconds)))
        h = seconds_int // 3600
        m = (seconds_int % 3600) // 60
        s = seconds_int % 60
        return f"{h:02d}:{m:02d}:{s:02d}"
