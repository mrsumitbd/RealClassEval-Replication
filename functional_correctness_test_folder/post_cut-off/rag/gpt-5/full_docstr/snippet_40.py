from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional


class SessionCalculator:
    """Handles session-related calculations for display purposes.
    (Moved from ui/calculators.py)"""

    def __init__(self) -> None:
        """Initialize session calculator."""
        self.default_cost_limit = 100.0

    def _to_utc(self, dt: Optional[datetime]) -> Optional[datetime]:
        if dt is None:
            return None
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    def _parse_time(self, value: Any) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return self._to_utc(value)
        if isinstance(value, (int, float)):
            ts = float(value)
            if ts > 1e12:  # milliseconds
                ts /= 1000.0
            return datetime.fromtimestamp(ts, tz=timezone.utc)
        if isinstance(value, str):
            s = value.strip()
            try:
                if s.endswith("Z"):
                    s = s[:-1] + "+00:00"
                # Python's fromisoformat handles offsets like +00:00
                dt = datetime.fromisoformat(s)
                return self._to_utc(dt)
            except Exception:
                # Fallback common formats
                fmts = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M:%S.%f",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%S.%f",
                ]
                for fmt in fmts:
                    try:
                        dt = datetime.strptime(s, fmt)
                        return self._to_utc(dt)
                    except Exception:
                        continue
        return None

    def _fmt_duration(self, seconds: Optional[float]) -> Optional[str]:
        if seconds is None:
            return None
        total = int(max(0, round(seconds)))
        days, rem = divmod(total, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, secs = divmod(rem, 60)
        parts = []
        if days:
            parts.append(f"{days}d")
        if hours:
            parts.append(f"{hours}h")
        if minutes:
            parts.append(f"{minutes}m")
        if secs or not parts:
            parts.append(f"{secs}s")
        return " ".join(parts)

    def calculate_time_data(self, session_data: Dict[str, Any], current_time: datetime) -> Dict[str, Any]:
        """Calculate time-related data for the session.
        Args:
            session_data: Dictionary containing session information
            current_time: Current UTC time
        Returns:
            Dictionary with calculated time data
        """
        now = self._to_utc(current_time)

        start_keys = ["start_time", "started_at", "created_at", "start"]
        end_keys = ["end_time", "ended_at",
                    "stopped_at", "stop_time", "finished_at"]
        last_activity_keys = ["heartbeat_at",
                              "last_activity_at", "last_heartbeat", "updated_at"]

        start_time = None
        for k in start_keys:
            if k in session_data:
                start_time = self._parse_time(session_data.get(k))
                if start_time:
                    break

        end_time = None
        for k in end_keys:
            if k in session_data:
                end_time = self._parse_time(session_data.get(k))
                if end_time:
                    break

        last_activity = None
        for k in last_activity_keys:
            if k in session_data:
                last_activity = self._parse_time(session_data.get(k))
                if last_activity:
                    break

        status = str(session_data.get("status", "")).lower()
        is_running = end_time is None
        if status in {"stopped", "completed", "terminated", "finished", "failed"}:
            is_running = False
        elif status in {"running", "active", "started"}:
            is_running = True

        effective_end = end_time or now
        if start_time:
            duration_seconds = max(
                0.0, (effective_end - start_time).total_seconds())
        else:
            duration_seconds = 0.0

        idle_seconds = None
        if last_activity:
            idle_seconds = max(0.0, (now - last_activity).total_seconds())

        return {
            "now": now,
            "now_iso": now.isoformat(),
            "start_time": start_time,
            "start_time_iso": start_time.isoformat() if start_time else None,
            "end_time": end_time,
            "end_time_iso": end_time.isoformat() if end_time else None,
            "is_running": is_running,
            "duration_seconds": duration_seconds,
            "elapsed_hours": duration_seconds / 3600.0,
            "elapsed_str": self._fmt_duration(duration_seconds),
            "last_activity": last_activity,
            "last_activity_iso": last_activity.isoformat() if last_activity else None,
            "idle_seconds": idle_seconds,
            "idle_str": self._fmt_duration(idle_seconds) if idle_seconds is not None else None,
        }

    def _extract_hourly_rate(self, session_data: Dict[str, Any]) -> float:
        rate_keys = [
            "cost_per_hour",
            "price_per_hour",
            "hourly_rate",
            "rate_per_hour",
        ]
        for k in rate_keys:
            v = session_data.get(k)
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                try:
                    return float(v)
                except Exception:
                    pass
        # Nested common locations
        pricing = session_data.get("pricing") or {}
        for k in ["hourly", "hourly_rate", "rate", "cost_per_hour"]:
            v = pricing.get(k)
            if isinstance(v, (int, float)):
                return float(v)
            if isinstance(v, str):
                try:
                    return float(v)
                except Exception:
                    pass
        return 0.0

    def _extract_cost_limit(self, session_data: Dict[str, Any], cost_limit: Optional[float]) -> float:
        if cost_limit is not None:
            return float(cost_limit)
        for k in ["cost_limit", "spending_limit", "budget", "max_cost"]:
            v = session_data.get(k)
            if v is not None:
                try:
                    return float(v)
                except Exception:
                    continue
        return self.default_cost_limit

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
        hourly_rate = self._extract_hourly_rate(session_data)
        elapsed_hours = float(time_data.get("elapsed_hours") or 0.0)
        is_running = bool(time_data.get("is_running"))
        now = time_data.get("now") or datetime.now(timezone.utc)

        # Use provided cost_so_far if present, else compute from elapsed time
        cost_so_far = None
        for k in ["cost_so_far", "accrued_cost", "spent", "total_cost"]:
            v = session_data.get(k)
            if isinstance(v, (int, float)):
                cost_so_far = float(v)
                break
            if isinstance(v, str):
                try:
                    cost_so_far = float(v)
                    break
                except Exception:
                    pass
        if cost_so_far is None:
            cost_so_far = hourly_rate * elapsed_hours

        limit = self._extract_cost_limit(session_data, cost_limit)
        remaining_budget = max(0.0, limit - cost_so_far)

        hours_until_limit = None
        projected_limit_time = None
        if is_running and hourly_rate > 0 and remaining_budget > 0:
            hours_until_limit = remaining_budget / hourly_rate
            projected_limit_time = now + timedelta(hours=hours_until_limit)

        will_hit_limit = bool(is_running and hourly_rate >
                              0 and remaining_budget > 0)

        return {
            "hourly_rate": hourly_rate,
            "elapsed_hours": elapsed_hours,
            "cost_so_far": cost_so_far,
            "cost_limit": limit,
            "remaining_budget": remaining_budget,
            "is_running": is_running,
            "hours_until_limit": hours_until_limit,
            "projected_limit_time": projected_limit_time,
            "projected_limit_time_iso": projected_limit_time.isoformat() if projected_limit_time else None,
            "will_hit_limit": will_hit_limit,
        }
